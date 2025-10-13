import os
from flask import Flask, json, render_template, request

app = Flask(__name__)

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "pokemon.json")

# Carga de datos del fichero JSON
with open(DATA_PATH, "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/lista', methods=["GET"])
def lista():
    trainer = request.args.get("trainer")  
    pokemon_list = app.config["DATA"]
    return render_template('Lista.html', pokemon=pokemon_list, trainer=trainer)



@app.route('/lista/<int:pokemon_id>')
def datos(pokemon_id):
    pokemon_list = app.config["DATA"]
    pokemon = next((poke for poke in pokemon_list if poke.get("id") == pokemon_id), None)
    return render_template('Datos.html', pokemon=pokemon) 

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)

app


# request form
#return redirect(url_for(..., ....))  