"""Logica de negocio de las respuestas del cuestionario (RF-04).

Las funciones reciben datos simples (modelos, ids, un dict con el formulario) y no
usan request ni abort: se pueden probar sin levantar Flask (ADR-05). Los errores se
comunican con excepciones propias y la ruta decide que codigo HTTP devolver.
"""
from sqlalchemy import case, func, or_
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.extensions import db
from app.models import Control, Pregunta, Respuesta
from app.services.scoring import RespuestaEvaluada

#Opciones (valor, texto) por tipo de pregunta. Es la unica fuente de verdad:
#el template dibuja los radios con ella y guardar_respuestas() valida contra ella.
OPCIONES_RESPUESTA = {
    "si_no_na": [("si", "Sí"), ("no", "No"), ("na", "N/A")],
    "frecuencia": [("diario", "Diario"), ("semanal", "Semanal"), ("mensual", "Mensual"), ("nunca", "Nunca")],
}

MAX_COMENTARIO = 1000


class RespuestaInvalida(Exception):
    """El formulario trae algo que la interfaz nunca envia (alguien altero el POST)."""


class SesionNoEditable(Exception):
    """La sesion no esta en_progreso: pausada (RF-03.3) o finalizada (RF-03.5)."""


def sesion_editable(sesion):
    #Solo se escribe en sesiones en_progreso; pausar/reanudar se hace desde /sesiones
    return sesion.estado_sesion == "en_progreso"


def respuestas_guardadas(id_sesion, id_control):
    """Respuestas ya guardadas de un control como {id_pregunta: Respuesta} (RF-04.5)."""
    respuestas = db.session.execute(
        db.select(Respuesta)
        .join(Pregunta)
        .where(Respuesta.id_sesion == id_sesion, Pregunta.id_control == id_control)
    ).scalars()
    return {r.id_pregunta: r for r in respuestas}


def progreso(id_sesion):
    """Avance de la sesion por control, ordenado por numero (RF-04.4, RF-04.7).

    Cada elemento: {"numero", "nombre", "total", "respondidas", "estado"} con
    estado en "completo", "parcial" o "pendiente".
    """
    filas = db.session.execute(
        db.select(
            Control.numero_control,
            Control.nombre_control,
            func.count(Pregunta.id_pregunta).label("total"),
            func.count(Respuesta.id_respuesta).label("respondidas"),
        )
        .join(Pregunta, Pregunta.id_control == Control.id_control)
        #LEFT JOIN: las preguntas sin respuesta tambien cuentan en el total
        .outerjoin(Respuesta, (Respuesta.id_pregunta == Pregunta.id_pregunta) & (Respuesta.id_sesion == id_sesion))
        .group_by(Control.id_control)
        .order_by(Control.numero_control)
    ).all()

    resultado = []
    for numero, nombre, total, respondidas in filas:
        if respondidas == total:
            estado = "completo"
        elif respondidas > 0:
            estado = "parcial"
        else:
            estado = "pendiente"
        resultado.append({"numero": numero, "nombre": nombre, "total": total, "respondidas": respondidas, "estado": estado})
    return resultado


def respuestas_para_scoring(id_sesion):
    """Respuestas de la sesion como RespuestaEvaluada, listas para scoring.calcular_scores (RF-05)."""
    filas = db.session.execute(
        db.select(Control.numero_control, Pregunta.criticidad_pregunta, Pregunta.tipo_respuesta, Respuesta.respuesta_valor)
        .join(Pregunta, Respuesta.id_pregunta == Pregunta.id_pregunta)
        .join(Control, Pregunta.id_control == Control.id_control)
        .where(Respuesta.id_sesion == id_sesion)
    ).all()
    return [RespuestaEvaluada(*fila) for fila in filas]


def guardar_respuestas(sesion, id_control, formulario):
    """Valida y guarda (upsert) las respuestas de un control.

    formulario: cualquier mapping con .get() (ej. request.form) con claves
    respuesta_<id_pregunta> y comentario_<id_pregunta>.
    Devuelve (guardadas, total_preguntas, comentarios_sin_respuesta).
    """
    if not sesion_editable(sesion):
        raise SesionNoEditable(f"La sesión está {sesion.estado_sesion} y no admite cambios.")

    #Se recorren las preguntas del control (no las claves del formulario): cualquier
    #campo extra o id de otro control que alguien agregue al POST simplemente se ignora
    preguntas = db.session.execute(db.select(Pregunta).filter_by(id_control = id_control)).scalars().all()

    filas = []
    comentarios_sin_respuesta = 0
    for pregunta in preguntas:
        valor = formulario.get(f"respuesta_{pregunta.id_pregunta}")
        #Comentario vacio o solo espacios se guarda como NULL (asi tambien se puede borrar)
        comentario = (formulario.get(f"comentario_{pregunta.id_pregunta}") or "").strip() or None

        if comentario is not None and len(comentario) > MAX_COMENTARIO:
            raise RespuestaInvalida(f"Comentario de la pregunta {pregunta.codigo_pregunta} demasiado largo.")
        if valor is None:
            #Sin respuesta no hay fila donde guardar el comentario (respuesta_valor es NOT NULL)
            if comentario is not None:
                comentarios_sin_respuesta += 1
            continue
        if valor not in {v for v, _ in OPCIONES_RESPUESTA[pregunta.tipo_respuesta]}:
            #Ej. "diario" en una pregunta si/no: el HTML nunca lo manda
            raise RespuestaInvalida(f"Valor '{valor}' no válido para la pregunta {pregunta.codigo_pregunta}.")

        filas.append({
            "id_sesion": sesion.id_sesion,
            "id_pregunta": pregunta.id_pregunta,
            "respuesta_valor": valor,
            "comentario_respuesta": comentario,
            "fecha_actualizacion": func.now(),
        })

    if filas:
        _upsert_respuestas(filas)
        db.session.commit()

    return len(filas), len(preguntas), comentarios_sin_respuesta


def _upsert_respuestas(filas):
    """INSERT ... ON CONFLICT (id_sesion, id_pregunta) DO UPDATE."""
    stmt = sqlite_insert(Respuesta).values(filas)
    nueva = stmt.excluded  #La fila que se intento insertar
    cambio_valor = Respuesta.respuesta_valor != nueva.respuesta_valor

    stmt = stmt.on_conflict_do_update(
        index_elements = [Respuesta.id_sesion, Respuesta.id_pregunta],
        set_ = {
            "respuesta_valor": nueva.respuesta_valor,
            "comentario_respuesta": nueva.comentario_respuesta,
            "fecha_actualizacion": func.now(),
            #Si el auditor cambio el valor ya no es del escaneo (RF-08.5); un comentario no cuenta
            "auto_completada": case((cambio_valor, False), else_ = Respuesta.auto_completada),
        },
        #Solo se toca la fila si algo cambio, asi fecha_actualizacion refleja cambios reales.
        #is_distinct_from compara bien contra NULL (comentario vacio)
        where = or_(cambio_valor, Respuesta.comentario_respuesta.is_distinct_from(nueva.comentario_respuesta)),
    )
    db.session.execute(stmt)
