import os
import random
from flask import Flask, current_app, json, render_template, request, redirect, url_for, session
from App.routes.pokemon_routes import pokemons_bp

app = Flask(__name__)
app.secret_key = "Pokemon-Battle"

# === CARGA DE DATOS ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "pokemon.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)

# === REGISTRO DEL BLUEPRINT ===
app.register_blueprint(pokemons_bp, url_prefix="/pokemons")

# === RUTA PRINCIPAL ===
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        trainer = request.form.get("trainer", "").strip()
        if trainer:
            session["trainer"] = trainer  # 🔹 Guardamos en sesión
            return redirect(url_for("pokemons_bp.lista"))  # 🔹 Vamos a /pokemons/lista
        else:
            return render_template("Home.html", errorNombre="Introduce un nombre válido.")
    return render_template("Home.html")

# === RUTA DE BATALLA ===
@app.route('/batalla', methods=['GET'])
def batalla():
    nombre = request.args.get("pokemon-combate", "").strip()
    trainer = session.get("trainer")  # ✅ usamos sesión en lugar de URL
    pokemon_list = current_app.config["DATA"]

    pokemon = next((poke for poke in pokemon_list if poke.get("name").lower() == nombre.lower()), None)

    if not trainer:
        return redirect(url_for('home'))

    if pokemon:
        enemigo = random.choice(pokemon_list)

        pokemon_moves = pokemon.copy()
        pokemon_moves["moves"] = random.sample(pokemon["moves"], min(4, len(pokemon["moves"])))

        enemigo_con_moves = enemigo.copy()
        enemigo_con_moves["moves"] = random.sample(enemigo["moves"], min(4, len(enemigo["moves"])))

        return render_template(
            "batalla.html",
            pokemon=pokemon_moves,
            trainer=trainer, # CORRECCIÓN 1: Usamos 'trainer' en lugar de 'entrenador'
            enemigo=enemigo_con_moves
        )
    else:
        errorCombate = f"No se encontró un Pokémon con el nombre '{nombre}'."
        # CORRECCIÓN 2: Usamos 'trainer' en lugar de 'entrenador' al devolver error a Lista.html
        return render_template("Lista.html", pokemon=pokemon_list, trainer=trainer, errorCombate=errorCombate)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)