from flask import Flask
from . import routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5d5f8e4f8f4a9e8f3b4d2f1c9a7e5b3c'  # Sample secret key, replace with your own

    with app.app_context():
        routes.init_app(app)
    
    return app
