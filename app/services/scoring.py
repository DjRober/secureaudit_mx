"""Calculo del score de riesgo de una auditoria (RF-05).

Funciones puras: reciben datos simples y devuelven numeros. No importan Flask ni la base
de datos, asi tests/test_scoring.py las prueba sin levantar la app (ADR-05, RNF-05.2).
La consulta que arma las respuestas vive en services/respuestas.py.

Regla (RF-05.2): cada respuesta suma puntos de riesgo segun la criticidad de su pregunta,
y el score es puntos / puntos posibles * 100 (0 = sin riesgo, 100 = riesgo maximo).

Decision de diseño — N/A no cuenta en los puntos posibles. Si contara, cada N/A bajaria el
riesgo como si fuera un "Si": un control con 1 "No" en pregunta Alta y 4 N/A daria 20 %
(Bajo, verde) en lugar de 100 % (Critico). Por lo mismo, un control con todo N/A (o sin
respuestas) no tiene score: es None ("no evaluable"), no 0 %. Un 0 % en verde le diria al
directivo que el control esta bien cuando nadie lo evaluo. Es el mismo razonamiento por el
que la 11.4 ya no ofrece N/A (modelo_datos.md, seccion 5).
"""
from typing import NamedTuple, Optional

#Puntos de un "No" segun la criticidad (RF-05.2). "Si" y "N/A" suman 0
PUNTOS_NO = {"Alta": 3, "Media": 2, "Baja": 1}

#Pregunta de frecuencia 11.4 (tipo_respuesta "frecuencia", sin N/A). Sus puntos son fijos
#por valor (RF-05.2), no dependen de la criticidad: el maximo es 3, igual que un "No" Alta
PUNTOS_FRECUENCIA = {"nunca": 3, "mensual": 3, "semanal": 1, "diario": 0}

#Niveles de RF-05.4 de mayor a menor, escritos como "desde X %" para que no queden huecos
#entre rangos (leido literalmente, 74.5 no esta ni en "50-74" ni en ">= 75")
NIVELES = ((75, "Crítico"), (50, "Alto"), (25, "Medio"), (0, "Bajo"))

#Color del semaforo de cada nivel. RF-06.1 pide tres colores para los cuatro niveles:
#Alto y Critico comparten el rojo y el texto del nivel los distingue
SEMAFORO = {"Crítico": "rojo", "Alto": "rojo", "Medio": "amarillo", "Bajo": "verde"}


class RespuestaEvaluada(NamedTuple):
    """Una respuesta con lo necesario para puntuarla."""
    control: int     #numero_control (1-18)
    criticidad: str  #"Alta", "Media" o "Baja"
    tipo: str        #"si_no_na" o "frecuencia"
    valor: str       #respuesta_valor


class ScoreControl(NamedTuple):
    score: Optional[float]  #0-100 con un decimal; None si no hay preguntas aplicables
    puntos: int             #puntos de riesgo obtenidos
    maximo: int             #puntos posibles: solo respuestas aplicables (sin N/A)
    respondidas: int        #respuestas recibidas, incluidas las N/A


class ScoreAuditoria(NamedTuple):
    score_global: Optional[float]
    por_control: dict[int, ScoreControl]  #{numero_control: ScoreControl}, ordenado por numero


def puntuar(criticidad, tipo, valor):
    """(puntos, maximo) de una respuesta segun RF-05.2. Una N/A devuelve (0, 0).

    Lanza ValueError ante una combinacion que la interfaz nunca envia (por ejemplo
    "diario" en una pregunta Si/No, o "na" en la 11.4).
    """
    if criticidad not in PUNTOS_NO:
        raise ValueError(f"Criticidad desconocida: {criticidad!r}")

    if tipo == "si_no_na":
        tabla = {"si": 0, "no": PUNTOS_NO[criticidad], "na": 0}
        maximo = 0 if valor == "na" else PUNTOS_NO[criticidad]
    elif tipo == "frecuencia":
        tabla = PUNTOS_FRECUENCIA
        maximo = max(PUNTOS_FRECUENCIA.values())
    else:
        raise ValueError(f"Tipo de respuesta desconocido: {tipo!r}")

    if valor not in tabla:
        raise ValueError(f"Valor {valor!r} no válido para una pregunta de tipo {tipo!r}")
    return tabla[valor], maximo


def calcular_scores(respuestas, controles=()):
    """Score de riesgo por control y global (RF-05.3).

    respuestas: iterable de RespuestaEvaluada (o tuplas en el mismo orden, como las filas
        de una consulta).
    controles: numeros de control en el alcance de la sesion. Un control sin respuestas
        solo aparece en el resultado si viene aqui, con score None.

    El global es la suma de puntos entre la suma de puntos posibles de todas las
    respuestas, no el promedio de los controles: asi la criticidad pondera igual en el
    global que dentro de cada control, y un control de 3 preguntas no pesa lo mismo que
    uno de 5.
    """
    acumulado = {numero: [0, 0, 0] for numero in controles}  #[puntos, maximo, respondidas]
    for control, criticidad, tipo, valor in respuestas:
        puntos, maximo = puntuar(criticidad, tipo, valor)
        fila = acumulado.setdefault(control, [0, 0, 0])
        fila[0] += puntos
        fila[1] += maximo
        fila[2] += 1

    por_control = {
        numero: ScoreControl(_porcentaje(puntos, maximo), puntos, maximo, respondidas)
        for numero, (puntos, maximo, respondidas) in sorted(acumulado.items())
    }
    total_puntos = sum(s.puntos for s in por_control.values())
    total_maximo = sum(s.maximo for s in por_control.values())
    return ScoreAuditoria(_porcentaje(total_puntos, total_maximo), por_control)


def nivel_riesgo(score):
    """Nivel de RF-05.4 ("Crítico", "Alto", "Medio", "Bajo"); None si no es evaluable."""
    if score is None:
        return None
    if not 0 <= score <= 100:
        raise ValueError(f"Score fuera de rango: {score!r}")
    for umbral, nivel in NIVELES:
        if score >= umbral:
            return nivel


def _porcentaje(puntos, maximo):
    #Sin respuestas aplicables no hay score (ver la decision de diseño arriba)
    if maximo == 0:
        return None
    #Un decimal. El nivel se calcula sobre este mismo valor ya redondeado, asi el numero
    #que se muestra y el color del semaforo nunca se contradicen (74.96 no se ve "75" en Alto)
    return round(puntos * 100 / maximo, 1)
