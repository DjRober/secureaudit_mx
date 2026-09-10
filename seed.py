from app import create_app
from app.extensions import db
from sqlalchemy import insert, select, func
from app.models import Control, Pregunta
import json
from pathlib import Path

SEEDS = Path(__file__).resolve().parent / "seeds"
controles = json.loads((SEEDS / "controles.json").read_text(encoding="utf-8"))
preguntas = json.loads((SEEDS / "preguntas.json").read_text(encoding="utf-8"))


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Controles y preguntas aqui
        count_controles = db.session.scalar(select(func.count()).select_from(Control))
        count_preguntas = db.session.scalar(select(func.count()).select_from(Pregunta))

        if(not count_controles):
            db.session.execute(insert(Control), controles)

        if(not count_preguntas):
            db.session.execute(insert(Pregunta), preguntas)

        db.session.commit()


if __name__ == "__main__":
    seed()