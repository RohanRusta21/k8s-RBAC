from flask import Flask, render_template
from kubernetes import client, config
import os

app = Flask(__name__)

def load_kube_config():
    # Check if the KUBECONFIG environment variable is set
    kubeconfig_path = os.getenv('KUBECONFIG', '/root/.kube/config')
    
    if not os.path.isfile(kubeconfig_path):
        raise FileNotFoundError(f"Kubeconfig file not found at {kubeconfig_path}")
    
    # Load kubeconfig file
    config.load_kube_config(config_file=kubeconfig_path)

@app.route('/')
def index():
    try:
        # Load the kubeconfig
        load_kube_config()
        
        # Example of accessing Kubernetes resources
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
        
        # Example: Print pod names (You can modify this to display data in the template)
        pod_names = [pod.metadata.name for pod in pods.items]
        
        return render_template('index.html', pod_names=pod_names)
    except FileNotFoundError as e:
        return f"Error: {str(e)}", 500
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
