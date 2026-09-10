from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import ForeignKey, Enum, func
from typing import List, Literal, Optional
import datetime

Estados_sesion = Literal["en_progreso", "pausada", "finalizada"]

class Sesion(db.Model):
    __tablename__ = "sesiones"

    #id_sesion	INTEGER	PK, AUTOINCREMENT	Identificador único de la sesión de auditoría
    id_sesion: Mapped[int] = mapped_column(primary_key=True)
    #id_empresa	INTEGER	FK → empresas.id_empresa, NOT NULL	Empresa auditada
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresas.id_empresa"))
    #id_usuario	INTEGER	FK → usuarios.id_usuario, NOT NULL	Usuario que ejecuta la auditoría
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    #fecha_inicio	DATETIME	NOT NULL, DEFAULT CURRENT_TIMESTAMP	Fecha de inicio de la auditoría
    fecha_inicio: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    #fecha_fin	DATETIME	NULLABLE	Fecha de finalización (NULL mientras esté en progreso)
    fecha_fin: Mapped[Optional[datetime.datetime]]
    #estado_sesion	TEXT	NOT NULL, CHECK IN ('en_progreso','pausada','finalizada'), DEFAULT 'en_progreso'	Estado de la sesión (RF-03.3: pausar/reanudar; RF-03.5: finalizada = inmutable)4
    estado_sesion: Mapped[Estados_sesion] = mapped_column(Enum("en_progreso", "pausada", "finalizada", create_constraint=True), server_default="en_progreso")

    #Parents
    empresa: Mapped["Empresa"] = relationship(back_populates="sesiones")
    usuario: Mapped["Usuario"] = relationship(back_populates="sesiones")
    #Childs
    respuestas: Mapped[List["Respuesta"]] = relationship(back_populates="sesion")
    sesion_controles: Mapped[List["SesionControl"]] = relationship(back_populates="sesion")

    