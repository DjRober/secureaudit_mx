from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from sqlalchemy import ForeignKey, Enum
from typing import List, Optional, Literal

Criticidad = Literal["Alta", "Media", "Baja"]
Tipo_respuesta = Literal["si_no_na", "frecuencia"]

class Pregunta(db.Model):
    __tablename__ = "preguntas"

    # id_pregunta INTEGER   PK, AUTOINCREMENT
    id_pregunta: Mapped[int] = mapped_column(primary_key=True)

    # id_control INTEGER    FK → controles.id_control, NOT NULL
    id_control: Mapped[int] = mapped_column(ForeignKey("controles.id_control"))

    # codigo_pregunta   TEXT	NOT NULL, UNIQUE
    codigo_pregunta: Mapped[str] = mapped_column(unique=True)

    # texto_pregunta	TEXT	NOT NULL
    texto_pregunta: Mapped[str] 

    # cia_pregunta	TEXT	NOT NULL
    cia_pregunta: Mapped[str] 

    # criticidad_pregunta	TEXT	NOT NULL, CHECK IN ('Alta','Media','Baja')
    criticidad_pregunta: Mapped[Criticidad] = mapped_column(Enum("Alta","Media","Baja", create_constraint=True))

    # tipo_respuesta	TEXT	NOT NULL, CHECK IN ('si_no_na','frecuencia'), DEFAULT 'si_no_na'
    tipo_respuesta: Mapped[Tipo_respuesta] = mapped_column(Enum("si_no_na","frecuencia", create_constraint=True), server_default="si_no_na")

    # descripcion_ayuda	TEXT	NULLABLE
    descripcion_ayuda: Mapped[Optional[str]] 

    #Parents (SQLAlchemy)
    control: Mapped["Control"] = relationship(back_populates="preguntas")
    #Childs
    respuestas: Mapped[List["Respuesta"]] = relationship(back_populates="pregunta")