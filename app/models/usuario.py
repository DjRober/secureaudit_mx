from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import Enum, func
from typing import List, Literal, Optional
import datetime


Rol_usuario = Literal["auditor", "tecnico", "directivo"]

class Usuario(db.Model):
    __tablename__ = "usuarios"

    # id_usuario	INTEGER	PK, AUTOINCREMENT	Identificador único del usuario
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    #rol_usuario	TEXT	NOT NULL, CHECK IN ('auditor','tecnico','directivo')	Rol del usuario (RF-01.4): U01, U02, U03
    rol_usuario: Mapped[Rol_usuario] = mapped_column(Enum("auditor", "tecnico", "directivo", create_constraint=True))
    #nombre_usuario	TEXT	NOT NULL	Nombre(s)
    nombre_usuario: Mapped[str]
    #apellidoP_usuario	TEXT	NOT NULL	Apellido paterno
    apellidoP_usuario: Mapped[str]
    #apellidoM_usuario	TEXT	NULLABLE	Apellido materno
    apellidoM_usuario: Mapped[Optional[str]]
    #correo_usuario	TEXT	NOT NULL, UNIQUE	Correo electrónico (usado para login)
    correo_usuario: Mapped[str] = mapped_column(unique=True)
    #contraseña_usuario	TEXT	NOT NULL	Hash bcrypt de la contraseña
    contraseña_usuario: Mapped[str]
    #es_activo	BOOLEAN	NOT NULL, DEFAULT 1	Permite deshabilitar cuentas sin eliminarlas
    es_activo: Mapped[bool] = mapped_column(server_default="1")
    #intentos_fallidos	INTEGER	NOT NULL, DEFAULT 0	Contador para RF-01.7 (rate limiting)
    intentos_fallidos: Mapped[int] = mapped_column(server_default="0")
    #bloqueado_hasta	DATETIME	NULLABLE	Fecha/hora hasta la cual la cuenta está bloqueada (RF-01.7)
    bloqueado_hasta: Mapped[Optional[datetime.datetime]]
    #fecha_creacion	DATETIME	NOT NULL, DEFAULT CURRENT_TIMESTAMP	Auditoría interna del registro
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    #Childs
    empresas: Mapped[List["Empresa"]] = relationship(back_populates="usuario")
    sesiones: Mapped[List["Sesion"]] = relationship(back_populates="usuario")
    logs: Mapped[List["Log"]] = relationship(back_populates="usuario")
