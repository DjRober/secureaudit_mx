from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app.extensions import db
from app.models import Control, Pregunta

cuestionario_page = Blueprint("cuestionario_page", __name__, template_folder="templates")

@cuestionario_page.route("/cuestionario/control/<int:numero_control>")
def cuestionario_control(numero_control):
    try:
        control = db.get_or_404(Control, numero_control)
        preguntas = db.session.execute(db.select(Pregunta).filter_by(id_control = numero_control)).scalars().all()

        return render_template(f"cuestionario.html", control = control, preguntas = preguntas)
    except TemplateNotFound:
        abort(404)