from flask import Flask, render_template, request, redirect, url_for
from kubernetes import client, config
import os
import json

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
    rules_json = request.form['rules']

    try:
        load_kube_config()

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
        return redirect(url_for('index', message='Role created successfully'))
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
