from flask import Flask
from app.extensions import db, csrf, migrate
import os
import mimetypes
from app.routes import autentificacion_page, cuestionario_page

#En Windows, Python toma el tipo MIME del registro del sistema y en algunos equipos
#.js figura como text/plain: el navegador rechazaria los modulos ES (type="module")
#de static/js/. Se fija el tipo correcto para que funcione en cualquier equipo (RNF-04.1)
mimetypes.add_type("text/javascript", ".js")

def create_app():
    #Crear la app de flask
    app = Flask(__name__)
    
    #Configuraciones
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave_alternativa_de_desarrollo'
    #SQLite en instance/secureaudit.db. DATABASE_URL permite usar otra base (pruebas,
    #generar migraciones contra una base vacia) sin tocar la de desarrollo
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///secureaudit.db"
    #El token CSRF vale lo que dure la sesion (por defecto expira en 1 h y una
    #auditoria larga perderia sus respuestas al guardar)
    app.config["WTF_CSRF_TIME_LIMIT"] = None

    #Inicializando extensiones
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    #Blueprints
    app.register_blueprint(autentificacion_page)
    app.register_blueprint(cuestionario_page)

    # Routes
    @app.route("/ping")
    def ping():
        return {"status": "ok", "version": "1.0.0"}

    return app