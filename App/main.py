import os
from flask import Flask, flash, json, redirect, render_template, request, url_for

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
    trainer = request.args.get("trainer", "").strip()
    pokemon_list = app.config["DATA"]

    # Si no hay entrenador, no mostramos error
    if trainer and not (3 <= len(trainer) <= 15):
        errorNombre = "El nombre del entrenador debe tener entre 3 y 15 caracteres."
        return render_template("Home.html", errorNombre=errorNombre)

    return render_template('Lista.html', pokemon=pokemon_list, trainer=trainer)


@app.route('/lista/<int:pokemon_id>')
def datos(pokemon_id):
    pokemon_list = app.config["DATA"]
    pokemon = next((poke for poke in pokemon_list if poke.get("id") == pokemon_id), None)
    return render_template('Datos.html', pokemon=pokemon) 


@app.route('/batalla', methods=['GET'])
def batalla():
    nombre = request.args.get("pokemon-combate", "").strip()
    trainer = request.args.get("trainer", "").strip()
    pokemon_list = app.config["DATA"]


    pokemon = next((poke for poke in pokemon_list if poke.get("name").lower() == nombre.lower()), None)

    if pokemon: 
        # Si existe
        return render_template("batalla.html", pokemon=pokemon, trainer=trainer)
    else:
        # Si no existe
        errorCombate = f"No se encontró un Pokémon con el nombre '{nombre}'."
        return render_template("Lista.html", pokemon=pokemon_list, trainer=trainer, errorCombate=errorCombate)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)



# request form
#return redirect(url_for(..., ....))  