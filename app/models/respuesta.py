from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from typing import Literal, Optional
import datetime

Respuesta_valor = Literal["si", "no", "na", "diario", "semanal", "mensual"]

class Respuesta(db.Model):
    __tablename__ = "respuestas"

    #id_respuesta	INTEGER	PK, AUTOINCREMENT	Identificador único de la respuesta
    id_respuesta: Mapped[int] = mapped_column(primary_key=True)
    #id_sesion	INTEGER	FK → sesiones.id_sesion, NOT NULL	Sesión a la que pertenece
    id_sesion: Mapped[int] = mapped_column(ForeignKey("sesiones.id_sesion"))
    #id_pregunta	INTEGER	FK → preguntas.id_pregunta, NOT NULL	Pregunta respondida
    id_pregunta: Mapped[int] = mapped_column(ForeignKey("preguntas.id_pregunta"))
    #respuesta_valor	TEXT	NOT NULL, CHECK IN ('si','no','na','diario','semanal','mensual')	Valor de la respuesta
    respuesta_valor: Mapped[Respuesta_valor] = mapped_column(Enum("si", "no", "na", "diario", "semanal", "mensual", create_constraint=True))
    #comentario_respuesta	TEXT	NULLABLE	Observaciones del auditor
    comentario_respuesta: Mapped[Optional[str]]
    #auto_completada	BOOLEAN	NOT NULL, DEFAULT 0	Indica si fue llenada automáticamente por el escaneo (RF-08.5)
    auto_completada: Mapped[bool] = mapped_column(server_default="0")
    #fecha_actualizacion	DATETIME	NULLABLE	Última modificación manual del auditor (trazabilidad)
    fecha_actualizacion: Mapped[Optional[datetime.datetime]]

    #Parents
    sesion: Mapped["Sesion"] = relationship(back_populates="respuestas")
    pregunta: Mapped["Pregunta"] = relationship(back_populates="respuestas")

    #UNIQUE(id_sesion, id_pregunta) — una sesión no puede tener dos respuestas para la misma pregunta
    __table_args__ = (
        UniqueConstraint("id_sesion", "id_pregunta", name="uq_respuesta_sesion_pregunta"),
    )