from flask import Flask, render_template, request, redirect, url_for
from kubernetes import client, config
import os

app = Flask(__name__)

# Load Kubernetes configuration
def load_kube_config():
    kube_config_path = os.path.expanduser('~/.kube/config')
    if os.path.exists(kube_config_path):
        config.load_kube_config(config_file=kube_config_path)
    else:
        raise FileNotFoundError(f"Kube config file not found at {kube_config_path}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_role', methods=['POST'])
def create_role():
    namespace = request.form['namespace']
    role_name = request.form['role_name']
    rules = request.form['rules']

    try:
        load_kube_config()

        v1 = client.RbacAuthorizationV1Api()

        role = client.V1Role(
            metadata=client.V1ObjectMeta(name=role_name),
            rules=[client.V1PolicyRule(
                api_groups=[""],
                resources=["pods"],
                verbs=["get", "list", "watch"]
            )]
        )

        v1.create_namespaced_role(namespace=namespace, body=role)
        return redirect(url_for('index', message='Role created successfully'))
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
