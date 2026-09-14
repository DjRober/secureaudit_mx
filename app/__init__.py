from flask import Flask
from app.extensions import db
import logging

logging.debug("Entramos")

def create_app():
    # Create the app
    app = Flask(__name__)
    # Configure the SQLite database, relative to the app intance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secureaudit.db"
    # Initialize the app with the extension
    db.init_app(app)

    # Routes
    @app.route("/ping")
    def ping():
        return {"status": "ok", "version": "1.0.0"}

    

    return app