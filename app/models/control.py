from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from typing import List

class Control(db.Model):
    __tablename__ = "controles"

    #id_control | INTEGER | PK, AUTOINCREMENT
    id_control: Mapped[int] = mapped_column(primary_key=True)
    #numero_control | INTEGER | NOT NULL, UNIQUE
    numero_control: Mapped[int] = mapped_column(unique=True)
    #nombre_control | TEXT | NOT NULL
    nombre_control: Mapped[str]

    #Childs (SQLAlchemy)
    preguntas: Mapped[List["Pregunta"]] = relationship(back_populates="control")
    sesion_controles: Mapped[List["SesionControl"]] = relationship(back_populates="control")