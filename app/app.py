# Importar el modulo
from flask import Flask

# Declarar la variable para las instancias
app = Flask(__name__)

# Definir rutas
@app.route("/")
def hello():
    return "Hello, world! - secureaudit_mx"

if __name__ == "__main__": #Evitamos conflictos al importar
    app.run(debug=True)