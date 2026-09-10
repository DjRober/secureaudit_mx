from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import ForeignKey, Enum, func
from typing import List, Literal, Optional
import datetime

Tamaño_empresa = Literal["micro", "pequeña", "mediana"]

class Empresa(db.Model):
    __tablename__ = "empresas"

    #id_empresa	INTEGER	PK, AUTOINCREMENT	Identificador único de la empresa
    id_empresa: Mapped[int] = mapped_column(primary_key=True)
    #nombre_empresa	TEXT	NOT NULL	Razón social o nombre comercial
    nombre_empresa: Mapped[str]
    #sector_empresa	TEXT	NULLABLE	Giro/sector de la PyME
    sector_empresa: Mapped[Optional[str]]
    #tamaño_empresa	TEXT	NULLABLE, CHECK IN ('micro','pequeña','mediana')	Clasificación por tamaño
    tamaño_empresa: Mapped[Optional[Tamaño_empresa]] = mapped_column(Enum("micro", "pequeña", "mediana", create_constraint=True))
    #nombre_contacto_empresa	TEXT	NULLABLE	Persona de contacto
    nombre_contacto_empresa: Mapped[Optional[str]]
    #id_usuario_registro	INTEGER	FK → usuarios.id_usuario, NOT NULL	Usuario que dio de alta la empresa
    id_usuario_registro: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    #fecha_registro	DATETIME	NOT NULL, DEFAULT CURRENT_TIMESTAMP	Fecha de alta
    fecha_registro: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    #Parents
    usuario: Mapped["Usuario"] = relationship(back_populates="empresas")

    #Childs
    sesiones: Mapped[List["Sesion"]] = relationship(back_populates="empresa")