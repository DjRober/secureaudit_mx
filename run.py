# Importar el modulo
from app import create_app
from seed import seed
from werkzeug.serving import is_running_from_reloader

app = create_app()

if __name__ == "__main__": #Evitamos conflictos al importar
    #RNF-04.5: la base se crea e inicializa sola al arrancar, sin pasos manuales.
    #seed() aplica las migraciones pendientes y siembra los catalogos solo si faltan,
    #asi que en arranques posteriores no duplica nada.
    #Con debug=True el recargador de Werkzeug vuelve a ejecutar este archivo en un
    #proceso hijo (y otra vez con cada cambio de codigo): se inicializa solo en el
    #proceso original para que ocurra una vez por arranque
    if not is_running_from_reloader():
        seed(app)
    app.run(debug=True)
