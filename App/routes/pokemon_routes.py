from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

pokemons_bp = Blueprint('pokemons_bp', __name__)


@pokemons_bp.route('/lista', methods=["GET"])
def lista():
    # Verificar que el entrenador esté autenticado
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    # Obtener el nombre del entrenador de la sesión
    trainer = session['trainer']
    pokemon_list = current_app.config["DATA"]

    return render_template('Lista.html', pokemon=pokemon_list, trainer=trainer)


@pokemons_bp.route('/lista/<int:pokemon_id>')
def datos(pokemon_id):
    # Verificar que el entrenador esté autenticado
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    pokemon_list = current_app.config["DATA"]
    pokemon = next((poke for poke in pokemon_list if poke.get("id") == pokemon_id), None)
    
    if pokemon is None:
        return "Pokémon no encontrado", 404
    
    return render_template('Datos.html', pokemon=pokemon)