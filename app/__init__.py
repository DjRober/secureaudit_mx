from flask import Flask
from app.extensions import db, csrf
import os
from app.routes import autentificacion_page, cuestionario_page

def create_app():
    #Crear la app de flask
    app = Flask(__name__)
    
    #Configuraciones
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave_alternativa_de_desarrollo'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secureaudit.db" #SQLite database
    #El token CSRF vale lo que dure la sesion (por defecto expira en 1 h y una
    #auditoria larga perderia sus respuestas al guardar)
    app.config["WTF_CSRF_TIME_LIMIT"] = None

    #Inicializando extensiones
    db.init_app(app)
    csrf.init_app(app)

    #Blueprints
    app.register_blueprint(autentificacion_page)
    app.register_blueprint(cuestionario_page)

    # Routes
    @app.route("/ping")
    def ping():
        return {"status": "ok", "version": "1.0.0"}

    return app