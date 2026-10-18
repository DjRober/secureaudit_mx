from flask import Blueprint, render_template
from app.extensions import db
from app.models import Sesion
from app.routes.cuestionario import ID_SESION_DEMO
from app.services.respuestas import progreso, respuestas_para_scoring
from app.services.scoring import SEMAFORO, calcular_scores, nivel_riesgo

resultados_page = Blueprint("resultados_page", __name__, url_prefix="/resultados")

#Clase CSS de cada nivel (css/componentes/riesgo.css). None = no evaluable
CLASE_NIVEL = {"Crítico": "critico", "Alto": "alto", "Medio": "medio", "Bajo": "bajo", None: "ne"}

@resultados_page.get("")
def dashboard():
    #Dashboard (RF-06): score global con semaforo, radar y semaforo por control.
    #Se calcula en cada visita a partir de lo guardado, asi refleja el avance del cuestionario.
    #TEMPORAL: misma sesion demo que el cuestionario. Con login, la ruta recibira la sesion
    #y validara que el usuario pueda verla; el Directivo solo en lectura (RF-06.5)
    sesion = db.get_or_404(Sesion, ID_SESION_DEMO)
    avance = progreso(sesion.id_sesion)
    #TEMPORAL: todos los controles estan en el alcance, igual que en el cuestionario.
    #Con RF-03 seran los de sesion_controles (auditorias parciales del rol Tecnico)
    resultado = calcular_scores(respuestas_para_scoring(sesion.id_sesion), [c["numero"] for c in avance])

    controles = []
    for c in avance:
        score = resultado.por_control[c["numero"]].score
        nivel = nivel_riesgo(score)
        controles.append({**c, "score": score, "nivel": nivel, "clase": CLASE_NIVEL[nivel]})

    nivel_global = nivel_riesgo(resultado.score_global)
    return render_template(
        "resultados/dashboard.html",
        sesion = sesion,
        controles = controles,
        score_global = resultado.score_global,
        nivel_global = nivel_global,
        clase_global = CLASE_NIVEL[nivel_global],
        semaforo_global = SEMAFORO.get(nivel_global),
        respondidas = sum(c["respondidas"] for c in avance),
        total = sum(c["total"] for c in avance),
    )
