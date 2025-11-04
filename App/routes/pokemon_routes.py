from flask import Blueprint, render_template, request, current_app

pokemons_bp = Blueprint('pokemons_bp', __name__)


@pokemons_bp.route('/lista', methods=["GET"])
def lista():
    trainer = request.args.get("trainer", "").strip()
    pokemon_list = current_app.config["DATA"]

    # Si no hay entrenador, no mostramos error
    if trainer and not (3 <= len(trainer) <= 15):
        errorNombre = "El nombre del entrenador debe tener entre 3 y 15 caracteres."
        return render_template("Home.html", errorNombre=errorNombre)

    return render_template('Lista.html', pokemon=pokemon_list, trainer=trainer)


@pokemons_bp.route('/lista/<int:pokemon_id>')
def datos(pokemon_id):
    pokemon_list = current_app.config["DATA"]
    pokemon = next((poke for poke in pokemon_list if poke.get("id") == pokemon_id), None)
    
    if pokemon is None:
        return "Pokémon no encontrado", 404
    
    return render_template('Datos.html', pokemon=pokemon)