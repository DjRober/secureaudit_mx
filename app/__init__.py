from flask import Flask
from app.extensions import db
import os


def create_app():
    # Create the app
    app = Flask(__name__)
    
    # Configurations
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave_alternativa_de_desarrollo'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secureaudit.db" #SQLite database
    # Initialize the app with the extension
    db.init_app(app)

    # Routes
    @app.route("/ping")
    def ping():
        return {"status": "ok", "version": "1.0.0"}

    

    return app