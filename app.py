from flask import Flask, render_template, request, redirect, url_for, flash
from kubernetes import client, config

app = Flask(__name__)
app.secret_key = 'rohan123'  # This is required for flashing messages

# Load Kubernetes configuration
config.load_kube_config()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_role', methods=['GET', 'POST'])
def create_role():
    if request.method == 'POST':
        role_name = request.form['role_name']
        namespace = request.form['namespace']
        
        # Create Kubernetes API client
        rbac_api = client.RbacAuthorizationV1Api()

        # Define role object
        role = client.V1Role(
            metadata=client.V1ObjectMeta(name=role_name),
            rules=[client.V1PolicyRule(
                api_groups=["*"],
                resources=["*"],
                verbs=["*"]
            )]
        )

        try:
            # Create role in the specified namespace
            rbac_api.create_namespaced_role(namespace=namespace, body=role)
            flash(f'Role "{role_name}" created successfully in namespace "{namespace}".', 'success')
        except client.exceptions.ApiException as e:
            flash(f'Error creating role: {e}', 'danger')
        
        return redirect(url_for('index'))
    
    return render_template('create_role.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
