from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import ForeignKey, Enum, func
from typing import Optional
import datetime

class Log(db.Model):
    __tablename__ = "logs"

    #id_log	INTEGER	PK, AUTOINCREMENT	Identificador único del registro
    id_log: Mapped[int] = mapped_column(primary_key=True)
    #id_usuario	INTEGER	FK → usuarios.id_usuario, NULLABLE	Usuario que generó la acción (NULL en intentos de login fallidos con correo inexistente)
    id_usuario: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id_usuario"))
    #fecha_log	DATETIME	NOT NULL, DEFAULT CURRENT_TIMESTAMP	Fecha y hora del evento (RF-09.2)
    fecha_log: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    #accion_log	TEXT	NOT NULL	Acción realizada (login, logout, crear_sesion, generar_reporte, ejecutar_escaneo, crud_usuario, etc.)
    accion_log: Mapped[str]
    #resultado_log	TEXT	NOT NULL, CHECK IN ('exito','fallo')	Resultado de la acción
    resultado_log: Mapped[str] = mapped_column(Enum("exito", "fallo", create_constraint=True))
    #detalle_log	TEXT	NULLABLE	Información adicional (sin datos sensibles, RF-09.4)
    detalle_log: Mapped[Optional[str]]

    #Parents
    usuario: Mapped["Usuario"] = relationship(back_populates="logs")