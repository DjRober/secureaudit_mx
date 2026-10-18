"""Pruebas del calculo de riesgo (RF-05, RNF-05.2).

scoring.py es puro: las respuestas se arman a mano, sin app de Flask ni base de datos
(ADR-05). Los scores ya vienen redondeados a un decimal, por eso se comparan con ==.
"""
import subprocess
import sys
from pathlib import Path

import pytest

from app.services.scoring import (
    RespuestaEvaluada, ScoreControl, calcular_scores, nivel_riesgo, puntuar,
)


def r(control, criticidad, valor, tipo="si_no_na"):
    """Atajo para escribir una respuesta en una linea."""
    return RespuestaEvaluada(control, criticidad, tipo, valor)


@pytest.fixture
def catalogo():
    """Criticidades reales de los controles 1 y 2 (seeds/preguntas.json)."""
    return {
        1: ["Alta", "Media", "Alta", "Alta"],  #puntos posibles: 11
        2: ["Media", "Alta", "Alta", "Baja"],  #puntos posibles: 9
    }


def contestar_todo(catalogo, valor):
    return [r(control, criticidad, valor) for control, criticidades in catalogo.items() for criticidad in criticidades]


# ===== Los 6 casos minimos =====

def test_todo_si_es_riesgo_cero(catalogo):
    resultado = calcular_scores(contestar_todo(catalogo, "si"), list(catalogo))

    assert resultado.score_global == 0
    assert resultado.por_control == {1: ScoreControl(0, 0, 11, 4), 2: ScoreControl(0, 0, 9, 4)}
    assert nivel_riesgo(resultado.score_global) == "Bajo"


def test_todo_no_es_riesgo_maximo(catalogo):
    resultado = calcular_scores(contestar_todo(catalogo, "no"), list(catalogo))

    assert resultado.score_global == 100
    assert resultado.por_control == {1: ScoreControl(100, 11, 11, 4), 2: ScoreControl(100, 9, 9, 4)}
    assert nivel_riesgo(resultado.score_global) == "Crítico"


def test_mezcla_pondera_por_criticidad():
    respuestas = [
        #Control 1: 3 + 0 + 1 de 3 + 2 + 1 posibles (la N/A no cuenta) = 4/6
        r(1, "Alta", "no"), r(1, "Media", "si"), r(1, "Media", "na"), r(1, "Baja", "no"),
        #Control 2: 3 de 3 + 3 + 3 + 2 posibles = 3/11
        r(2, "Alta", "si"), r(2, "Alta", "si"), r(2, "Alta", "no"), r(2, "Media", "si"),
    ]
    resultado = calcular_scores(respuestas, [1, 2])

    assert resultado.por_control[1] == ScoreControl(66.7, 4, 6, 4)
    assert resultado.por_control[2] == ScoreControl(27.3, 3, 11, 4)
    #Global = 7/17, no el promedio de los controles (que daria 47.0)
    assert resultado.score_global == 41.2
    assert [nivel_riesgo(s.score) for s in resultado.por_control.values()] == ["Alto", "Medio"]


def test_todo_na_no_es_evaluable(catalogo):
    resultado = calcular_scores(contestar_todo(catalogo, "na"), list(catalogo))

    #None y no 0: con 0 % el semaforo saldria en verde sin que nada se haya evaluado
    assert resultado.score_global is None
    assert resultado.por_control == {1: ScoreControl(None, 0, 0, 4), 2: ScoreControl(None, 0, 0, 4)}
    assert nivel_riesgo(resultado.score_global) is None


def test_11_4_nunca_pesa_como_un_no_en_alta():
    #Control 11 real: 11.1-11.3 Si/No/N.A. en Alta + 11.4 de frecuencia
    con_nunca = [r(11, "Alta", "si")] * 3 + [r(11, "Alta", "nunca", tipo="frecuencia")]
    con_no = [r(11, "Alta", "si")] * 3 + [r(11, "Alta", "no")]

    assert calcular_scores(con_nunca).por_control[11] == ScoreControl(25.0, 3, 12, 4)
    assert calcular_scores(con_nunca) == calcular_scores(con_no)


def test_control_sin_respuestas():
    resultado = calcular_scores([r(1, "Alta", "no")], controles=[1, 2])

    assert resultado.por_control[2] == ScoreControl(None, 0, 0, 0)
    #El control sin respuestas no arrastra el global hacia ningun lado
    assert resultado.score_global == 100


# ===== Casos adicionales =====

def test_na_no_diluye_el_riesgo():
    #Control 3: 5 preguntas Alta. Si N/A contara en el maximo, esto daria 3/15 = 20 % (Bajo)
    respuestas = [r(3, "Alta", "no")] + [r(3, "Alta", "na")] * 4

    assert calcular_scores(respuestas).por_control[3] == ScoreControl(100, 3, 3, 5)


@pytest.mark.parametrize(("frecuencia", "score"), [
    ("nunca", 100),
    ("mensual", 100),
    ("semanal", 33.3),
    ("diario", 0),
])
def test_puntos_de_frecuencia(frecuencia, score):
    resultado = calcular_scores([r(11, "Alta", frecuencia, tipo="frecuencia")])

    assert resultado.por_control[11].score == score


def test_controles_sin_respuestas_y_fuera_de_alcance():
    #Solo aparecen los controles en alcance y los que tienen respuestas
    resultado = calcular_scores([r(5, "Media", "si")], controles=[1])

    assert list(resultado.por_control) == [1, 5]


def test_sin_respuestas_ni_controles():
    assert calcular_scores([]) == (None, {})


@pytest.mark.parametrize(("score", "nivel"), [
    (0, "Bajo"),
    (24.9, "Bajo"),
    (25, "Medio"),
    (49.9, "Medio"),
    (50, "Alto"),
    (74.9, "Alto"),
    (75, "Crítico"),
    (100, "Crítico"),
    (None, None),
])
def test_nivel_riesgo_en_las_fronteras(score, nivel):
    assert nivel_riesgo(score) == nivel


@pytest.mark.parametrize("score", [-0.1, 100.1])
def test_nivel_riesgo_fuera_de_rango(score):
    with pytest.raises(ValueError):
        nivel_riesgo(score)


@pytest.mark.parametrize(("criticidad", "tipo", "valor"), [
    ("Alta", "si_no_na", "diario"),    #valor de frecuencia en pregunta Si/No
    ("Alta", "frecuencia", "na"),      #la 11.4 no ofrece N/A
    ("Alta", "frecuencia", "no"),
    ("Extrema", "si_no_na", "no"),     #criticidad fuera del CHECK
    ("Alta", "abierta", "si"),         #tipo fuera del CHECK
])
def test_combinaciones_invalidas(criticidad, tipo, valor):
    with pytest.raises(ValueError):
        puntuar(criticidad, tipo, valor)


def test_scoring_no_importa_flask_ni_la_bd():
    #Se carga scoring.py por su ruta (sin pasar por app/__init__.py, que si importa Flask)
    #en un interprete limpio, y se revisa que no haya arrastrado Flask, SQLAlchemy ni app
    ruta = Path(__file__).resolve().parents[1] / "app" / "services" / "scoring.py"
    codigo = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('scoring', {str(ruta)!r})\n"
        "spec.loader.exec_module(importlib.util.module_from_spec(spec))\n"
        "print(sorted(m for m in sys.modules if m.split('.')[0] in {'flask', 'sqlalchemy', 'app'}))\n"
    )
    salida = subprocess.run([sys.executable, "-I", "-c", codigo], capture_output=True, text=True, check=True)

    assert salida.stdout.strip() == "[]"
