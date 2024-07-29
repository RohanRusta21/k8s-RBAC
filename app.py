from flask import Flask, request, render_template, redirect, url_for, flash
from kubernetes import client, config

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  # Change this to a secure key

# Load Kubernetes configuration
def load_kube_config():
    try:
        # Load the kube config from the default location or set your own path here
        config.load_kube_config()
    except Exception as e:
        print(f"Error loading kube config: {e}")

# Create a Kubernetes role
def create_role(namespace, role_name, api_groups, resources, verbs):
    try:
        load_kube_config()
        k8s_rbac_api = client.RbacAuthorizationV1Api()

        # Define role rules
        rules = [
            client.V1PolicyRule(
                api_groups=api_groups,
                resources=resources,
                verbs=verbs
            )
        ]

        # Define role
        role = client.V1Role(
            api_version="rbac.authorization.k8s.io/v1",
            kind="Role",
            metadata=client.V1ObjectMeta(name=role_name),
            rules=rules
        )

        # Create role
        k8s_rbac_api.create_namespaced_role(namespace, role)
        return True
    except Exception as e:
        print(f"Error creating role: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        namespace = request.form['namespace']
        role_name = request.form['role_name']
        api_groups = request.form.getlist('api_groups')
        resources = request.form.getlist('resources')
        verbs = request.form.getlist('verbs')

        # Create the role
        success = create_role(namespace, role_name, api_groups, resources, verbs)
        if success:
            flash('Role created successfully!', 'success')
        else:
            flash('Failed to create role.', 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
