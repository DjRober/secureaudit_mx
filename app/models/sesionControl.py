from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import ForeignKey

class SesionControl(db.Model):
    __tablename__ = "sesion_controles"

    #id_sesion	INTEGER	FK → sesiones.id_sesion, PK compuesta	Sesión
    id_sesion: Mapped[int] = mapped_column(ForeignKey("sesiones.id_sesion"), primary_key=True)
    #id_control	INTEGER	FK → controles.id_control, PK compuesta	Control incluido en el alcance de la sesión
    id_control: Mapped[int] = mapped_column(ForeignKey("controles.id_control"), primary_key=True)

    #Parents
    control: Mapped["Control"] = relationship(back_populates="sesion_controles")
    sesion: Mapped["Sesion"] = relationship(back_populates="sesion_controles")