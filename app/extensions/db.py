from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

#Convencion de nombres para las restricciones (ADR-03). Sin nombre, Alembic en modo
#batch (SQLite) no puede borrar ni reemplazar una restriccion en una migracion.
#
#No hay regla "ck" a proposito: los CHECK salen de los Enum, y cada Enum lleva su
#nombre completo en el modelo (ej. name="ck_respuestas_respuesta_valor"). En modo
#batch la convencion NO se aplica al CHECK de un tipo: Alembic busca el CHECK viejo
#por el name del Enum tal cual. Si la convencion lo renombrara, el nombre en la BD no
#coincidiria, el CHECK viejo no se borraria y el valor nuevo seguiria rechazado.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention = NAMING_CONVENTION)

db = SQLAlchemy(model_class=Base)
