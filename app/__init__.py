from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)

    # Config minimale 
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'dev'

    # Enregistrer le Blueprint
    app.register_blueprint(main)

    return app
