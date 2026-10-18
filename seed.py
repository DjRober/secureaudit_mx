from app import create_app
from app.extensions import db
from flask_migrate import upgrade
from sqlalchemy import insert, select, func
from app.models import Control, Pregunta, Usuario, Empresa, Sesion
import json
from pathlib import Path

SEEDS = Path(__file__).resolve().parent / "seeds"
controles = json.loads((SEEDS / "controles.json").read_text(encoding="utf-8"))
preguntas = json.loads((SEEDS / "preguntas.json").read_text(encoding="utf-8"))
demo = json.loads((SEEDS / "demo.json").read_text(encoding="utf-8"))


def seed():
    app = create_app()
    with app.app_context():
        # Esquema: se aplican las migraciones pendientes (equivale a "flask db upgrade").
        # Ya no se usa db.create_all(): crearia tablas sin registrar la version en
        # alembic_version y las migraciones posteriores no sabrian desde donde partir (ADR-03)
        upgrade()

        # Controles y preguntas aqui
        count_controles = db.session.scalar(select(func.count()).select_from(Control))
        count_preguntas = db.session.scalar(select(func.count()).select_from(Pregunta))

        if(not count_controles):
            db.session.execute(insert(Control), controles)

        if(not count_preguntas):
            db.session.execute(insert(Pregunta), preguntas)

        # Datos demo (TEMPORAL hasta tener login): usuario + empresa + sesion id 1, que usa
        # ID_SESION_DEMO en app/routes/cuestionario.py. La contraseña "!" no es un hash
        # bcrypt valido a proposito: esta cuenta nunca podra iniciar sesion.
        count_usuarios = db.session.scalar(select(func.count()).select_from(Usuario))

        if(not count_usuarios):
            db.session.execute(insert(Usuario), demo["usuarios"])
            db.session.execute(insert(Empresa), demo["empresas"])
            db.session.execute(insert(Sesion), demo["sesiones"])

        db.session.commit()


if __name__ == "__main__":
    seed()