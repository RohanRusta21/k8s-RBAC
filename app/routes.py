from flask import render_template, request, flash, redirect, url_for
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def init_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/create_role', methods=['GET', 'POST'])
    def create_role():
        if request.method == 'POST':
            role_name = request.form.get('role_name')
            if role_name:
                try:
                    config.load_kube_config()  # Load kubeconfig from default location
                    rbac_v1 = client.RbacAuthorizationV1Api()
                    body = client.V1Role(
                        metadata=client.V1ObjectMeta(name=role_name),
                        rules=[client.V1PolicyRule(
                            api_groups=[""],
                            resources=["pods"],
                            verbs=["get", "list", "watch"]
                        )]
                    )
                    rbac_v1.create_namespaced_role(namespace='default', body=body)
                    flash('Role created successfully', 'success')
                except ApiException as e:
                    flash(f"Exception when creating role: {e}", 'danger')
                return redirect(url_for('index'))
        return render_template('create_role.html')
