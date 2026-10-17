from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

autentificacion_page = Blueprint("autentificacion_page", __name__, template_folder="templates")

#Pruebas de my first blueprint (temporal)
@autentificacion_page.route("/auth")
def show():
    try:
        return render_template("auth.html")
    except TemplateNotFound:
        abort(404)



