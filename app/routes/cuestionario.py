from flask import Blueprint, render_template
from app.extensions import db
from app.models import Control, Pregunta

cuestionario_page = Blueprint("cuestionario_page", __name__, url_prefix="/cuestionario")

@cuestionario_page.route("/control/<int:numero_control>")
def cuestionario_control(numero_control):
    #Se busca por numero_control (el que ve el usuario), no por la PK id_control
    control = db.first_or_404(db.select(Control).filter_by(numero_control = numero_control))
    preguntas = db.session.execute(
        db.select(Pregunta).filter_by(id_control = control.id_control).order_by(Pregunta.id_pregunta)
    ).scalars().all()

    return render_template("cuestionario.html", control = control, preguntas = preguntas)
