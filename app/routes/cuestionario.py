from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from sqlalchemy import func
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.extensions import db
from app.models import Control, Pregunta, Respuesta, Sesion

cuestionario_page = Blueprint("cuestionario_page", __name__, url_prefix="/cuestionario")

#TEMPORAL: mientras no exista login, todas las respuestas se guardan en la sesion demo
#que crea seed.py. Con auth, esto se reemplaza por la sesion activa del usuario.
ID_SESION_DEMO = 1

#Opciones (valor, texto) por tipo de pregunta. Es la unica fuente de verdad:
#el template dibuja los radios con ella y guardar() valida contra ella.
OPCIONES_RESPUESTA = {
    "si_no_na": [("si", "Sí"), ("no", "No"), ("na", "N/A")],
    "frecuencia": [("diario", "Diario"), ("semanal", "Semanal"), ("mensual", "Mensual"), ("na", "N/A")],
}

@cuestionario_page.route("/control/<int:numero_control>")
def cuestionario_control(numero_control):
    #Se busca por numero_control (el que ve el usuario), no por la PK id_control
    control = db.first_or_404(db.select(Control).filter_by(numero_control = numero_control))
    preguntas = db.session.execute(
        db.select(Pregunta).filter_by(id_control = control.id_control).order_by(Pregunta.id_pregunta)
    ).scalars().all()

    #Respuestas ya guardadas de este control como {id_pregunta: valor}, para marcarlas al volver (RF-04.5)
    respuestas = dict(db.session.execute(
        db.select(Respuesta.id_pregunta, Respuesta.respuesta_valor)
        .join(Pregunta)
        .where(Respuesta.id_sesion == ID_SESION_DEMO, Pregunta.id_control == control.id_control)
    ).all())

    return render_template(
        "cuestionario.html",
        control = control,
        preguntas = preguntas,
        respuestas = respuestas,
        opciones = OPCIONES_RESPUESTA,
    )

@cuestionario_page.post("/guardar")
def guardar():
    #numero_control llega en un input hidden; con type=int, si no es un entero devuelve None
    numero_control = request.form.get("numero_control", type = int)
    if numero_control is None:
        abort(400)
    control = db.first_or_404(db.select(Control).filter_by(numero_control = numero_control))

    #RF-03.5: una sesion finalizada no puede modificarse
    sesion = db.get_or_404(Sesion, ID_SESION_DEMO)
    if sesion.estado_sesion == "finalizada":
        abort(409, description = "La sesión está finalizada y ya no admite cambios.")

    #Se recorren las preguntas del control (no las claves del formulario): cualquier
    #campo extra o id de otro control que alguien agregue al POST simplemente se ignora
    preguntas = db.session.execute(
        db.select(Pregunta).filter_by(id_control = control.id_control)
    ).scalars().all()

    filas = []
    for pregunta in preguntas:
        valor = request.form.get(f"respuesta_{pregunta.id_pregunta}")
        if valor is None:
            continue  #Pregunta sin contestar: no se guarda nada
        valores_validos = {v for v, _ in OPCIONES_RESPUESTA[pregunta.tipo_respuesta]}
        if valor not in valores_validos:
            abort(400)  #Ej. "diario" en una pregunta si/no: el HTML nunca lo manda, alguien altero el POST
        filas.append({
            "id_sesion": sesion.id_sesion,
            "id_pregunta": pregunta.id_pregunta,
            "respuesta_valor": valor,
            "fecha_actualizacion": func.now(),
        })

    if filas:
        #Upsert: INSERT ... ON CONFLICT (id_sesion, id_pregunta) DO UPDATE
        stmt = sqlite_insert(Respuesta).values(filas)
        stmt = stmt.on_conflict_do_update(
            index_elements = [Respuesta.id_sesion, Respuesta.id_pregunta],
            set_ = {
                "respuesta_valor": stmt.excluded.respuesta_valor,
                "fecha_actualizacion": func.now(),
                "auto_completada": False,  #El auditor la cambio a mano: ya no es del escaneo (RF-08.5)
            },
            #Solo se actualiza si el valor cambio, asi fecha_actualizacion refleja cambios reales
            where = Respuesta.respuesta_valor != stmt.excluded.respuesta_valor,
        )
        db.session.execute(stmt)
        db.session.commit()
        flash(f"Control {control.numero_control}: {len(filas)} de {len(preguntas)} respuestas guardadas.", "exito")
    else:
        flash(f"Control {control.numero_control}: no marcaste ninguna respuesta.", "aviso")

    #Post/Redirect/Get: tras el POST siempre se redirige, asi F5 no reenvia el formulario
    siguiente = db.session.scalar(db.select(Control).filter_by(numero_control = control.numero_control + 1))
    if siguiente is None:
        flash("Este es el último control del cuestionario.", "aviso")
        return redirect(url_for(".cuestionario_control", numero_control = control.numero_control))
    return redirect(url_for(".cuestionario_control", numero_control = siguiente.numero_control))
