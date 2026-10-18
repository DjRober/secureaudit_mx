from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.extensions import db
from app.models import Control, Pregunta, Sesion
from app.services.respuestas import (
    OPCIONES_RESPUESTA, MAX_COMENTARIO, RespuestaInvalida, SesionNoEditable,
    guardar_respuestas, progreso, respuestas_guardadas, sesion_editable,
)

cuestionario_page = Blueprint("cuestionario_page", __name__, url_prefix="/cuestionario")

#TEMPORAL: mientras no exista login, todas las respuestas se guardan en la sesion demo
#que crea seed.py. Con auth, esto se reemplaza por la sesion activa del usuario.
ID_SESION_DEMO = 1

@cuestionario_page.route("/control/<int:numero_control>")
def cuestionario_control(numero_control):
    #Se busca por numero_control (el que ve el usuario), no por la PK id_control
    control = db.first_or_404(db.select(Control).filter_by(numero_control = numero_control))
    preguntas = db.session.execute(
        db.select(Pregunta).filter_by(id_control = control.id_control).order_by(Pregunta.id_pregunta)
    ).scalars().all()
    sesion = db.get_or_404(Sesion, ID_SESION_DEMO)

    return render_template(
        "cuestionario/control.html",
        control = control,
        preguntas = preguntas,
        respuestas = respuestas_guardadas(sesion.id_sesion, control.id_control),
        progreso = progreso(sesion.id_sesion),
        editable = sesion_editable(sesion),
        opciones = OPCIONES_RESPUESTA,
        max_comentario = MAX_COMENTARIO,
    )

@cuestionario_page.post("/guardar")
def guardar():
    #numero_control: control que se esta contestando. destino: a que control ir despues
    #(anterior, siguiente o uno del navegador). Con type=int, si no es entero devuelve None
    numero_control = request.form.get("numero_control", type = int)
    destino = request.form.get("destino", type = int)
    if numero_control is None:
        abort(400)
    control = db.first_or_404(db.select(Control).filter_by(numero_control = numero_control))
    sesion = db.get_or_404(Sesion, ID_SESION_DEMO)

    try:
        guardadas, total, sin_respuesta = guardar_respuestas(sesion, control.id_control, request.form)
    except SesionNoEditable as error:
        abort(409, description = str(error))
    except RespuestaInvalida as error:
        abort(400, description = str(error))

    if guardadas:
        flash(f"Control {control.numero_control}: {guardadas} de {total} respuestas guardadas.", "exito")
    if sin_respuesta:
        flash(f"{sin_respuesta} comentario(s) no se guardaron porque su pregunta no tiene respuesta.", "aviso")

    #Post/Redirect/Get: tras el POST siempre se redirige, asi F5 no reenvia el formulario.
    #Si el destino no existe (o no vino), se queda en el mismo control
    existe_destino = destino is not None and db.session.scalar(
        db.select(Control.id_control).filter_by(numero_control = destino)
    )
    siguiente = destino if existe_destino else control.numero_control
    return redirect(url_for(".cuestionario_control", numero_control = siguiente))
