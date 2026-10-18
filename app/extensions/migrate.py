from pathlib import Path
from flask_migrate import Migrate

#Migraciones de esquema con Alembic (ADR-03). Desde Flask-Migrate 4.0 el modo batch
#(render_as_batch) viene activo por defecto: SQLite no soporta la mayoria de los ALTER
#TABLE, asi que cada cambio recrea la tabla y copia los datos. Se deja explicito.
#La carpeta se da como ruta absoluta: por defecto es relativa al directorio actual y
#fallaria al correr seed.py o "flask db" desde otra carpeta.
MIGRACIONES = Path(__file__).resolve().parents[2] / "migrations"

migrate = Migrate(directory = str(MIGRACIONES), render_as_batch = True)
