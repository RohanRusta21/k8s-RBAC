from flask import Flask, render_template, request, redirect, url_for
from kubernetes import client, config
import os
import json
import tempfile

app = Flask(__name__)

# Load Kubernetes configuration
def load_kube_config(kubeconfig_path):
    if os.path.exists(kubeconfig_path):
        config.load_kube_config(config_file=kubeconfig_path)
    else:
        raise FileNotFoundError(f"Kube config file not found at {kubeconfig_path}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_role', methods=['POST'])
def create_role():
    namespace = request.form['namespace']
    role_name = request.form['role_name']
    rules_json = request.form['rules']
    kubeconfig_file = request.files['kubeconfig']

    try:
        # Save the uploaded kubeconfig file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.kubeconfig') as temp_kubeconfig:
            temp_kubeconfig.write(kubeconfig_file.read())
            temp_kubeconfig_path = temp_kubeconfig.name

        # Load the kubeconfig file
        load_kube_config(temp_kubeconfig_path)

        v1 = client.RbacAuthorizationV1Api()

        rules = json.loads(rules_json)
        policy_rules = [client.V1PolicyRule(
            api_groups=rule.get('apiGroups', []),
            resources=rule.get('resources', []),
            verbs=rule.get('verbs', [])
        ) for rule in rules]

        role = client.V1Role(
            metadata=client.V1ObjectMeta(name=role_name),
            rules=policy_rules
        )

        v1.create_namespaced_role(namespace=namespace, body=role)

        # Remove the temporary kubeconfig file
        os.remove(temp_kubeconfig_path)

        return redirect(url_for('index', message='Role created successfully'))
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
