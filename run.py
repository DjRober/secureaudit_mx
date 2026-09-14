# Importar el modulo
from app import create_app

app = create_app()

@app.route("/")
def hello():
        return "Hello, world! - secureaudit_mx"

if __name__ == "__main__": #Evitamos conflictos al importar
    app.run(debug=True)