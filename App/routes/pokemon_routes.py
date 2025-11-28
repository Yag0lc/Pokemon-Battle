from flask import Blueprint, app, render_template, request, current_app, session, redirect, url_for
from app.services.pokemon_service import obtener_pokemon_por_id, buscar_por_nombre


pokemons_bp_lista = Blueprint('pokemons_bp_lista', __name__)



@pokemons_bp_lista.route('/lista', methods=["GET"])
def lista():
    # Verificar que el entrenador esté autenticado
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    # Obtener el nombre del entrenador de la sesión
    trainer = session['trainer']
    pokemon_list = current_app.config["DATA"]

    return render_template('Lista.html', pokemon=pokemon_list, trainer=trainer)


@pokemons_bp_lista.route('/lista/<int:pokemon_id>')
def datos(pokemon_id):
    # Verificar que el entrenador esté autenticado
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    pokemon = obtener_pokemon_por_id(pokemon_id)
    
    if pokemon is None:
        return "Pokémon no encontrado", 404
    
    return render_template('Datos.html', pokemon=pokemon)


@pokemons_bp_lista.route('/seleccionar_pokemon', methods=['POST'])
def guardar_pokemon():
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    pokemon_nombre = request.form.get('pokemon', '').strip()
    


    if buscar_por_nombre(pokemon_nombre):
        if session.get('pokemon_seleccionado') != pokemon_nombre:
            session.pop('batalla_actual', None) 
            
        session['pokemon_seleccionado'] = pokemon_nombre
        return redirect(url_for('pokemons_bp_batalla.batalla'))
    else:
        return redirect(url_for('pokemons_bp_lista.lista'))