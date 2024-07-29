from flask import Flask, request, jsonify, send_from_directory
from kubernetes import client, config
import os

app = Flask(__name__)

def load_kube_config():
    kubeconfig_path = os.path.expanduser('~/.kube/config')
    if not os.path.exists(kubeconfig_path):
        raise Exception("Kubeconfig file not found.")
    # Load kubeconfig and disable SSL verification if needed
    config.load_kube_config(config_file=kubeconfig_path, verify_ssl=False)

def initialize_kube_client():
    try:
        load_kube_config()
        global k8s_client
        k8s_client = client.RbacAuthorizationV1Api()
    except Exception as e:
        app.logger.error(f"Error loading kube config: {e}")
        raise

@app.get('/')
def index():
    initialize_kube_client()
    return 'Kubernetes Role Manager is ready!'

@app.post('/create_role')
def create_role():
    try:
        # Get role definition from request
        role_definition = request.json
        namespace = role_definition.get('namespace', 'default')

        # Create the role
        role = client.V1Role(
            metadata=client.V1ObjectMeta(name=role_definition['name']),
            rules=role_definition['rules']
        )
        k8s_client.create_namespaced_role(namespace=namespace, body=role)

        return jsonify({"status": "Role created successfully"}), 201
    except Exception as e:
        app.logger.error(f"Error creating role: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
