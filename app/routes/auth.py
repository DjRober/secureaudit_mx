from flask import Blueprint, render_template

autentificacion_page = Blueprint("autentificacion_page", __name__, url_prefix="/auth")

#Pruebas de my first blueprint (temporal)
@autentificacion_page.route("/")
def show():
    return render_template("auth/login.html")
