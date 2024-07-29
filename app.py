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
def create_role(namespace, role_name, rules):
    try:
        load_kube_config()
        k8s_rbac_api = client.RbacAuthorizationV1Api()

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
        rules = request.form['rules']

        # Convert rules from string to a list of dictionaries
        try:
            rules_list = eval(rules)  # Use eval to convert string to list of dicts
            if not isinstance(rules_list, list):
                raise ValueError("Rules must be a list of dictionaries")

            # Create the role
            success = create_role(namespace, role_name, rules_list)
            if success:
                flash('Role created successfully!', 'success')
            else:
                flash('Failed to create role.', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
