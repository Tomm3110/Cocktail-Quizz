from flask import Flask
from .routes import main
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    #Initialisation de la BD
    init_db()

    # Enregistrer le Blueprint
    app.register_blueprint(main)

    return app
