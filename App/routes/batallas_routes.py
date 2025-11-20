import random
from flask import Blueprint, app, render_template, request, current_app, session, redirect, url_for
from App.repositories.pokemon_repo import buscar_por_id,buscar_por_nombre
from App.models.batalla import Batalla
from App.routes.pokemon_routes import pokemons_bp_lista

pokemons_bp_batalla = Blueprint('pokemons_bp_batalla', __name__)



# === RUTA DE BATALLA (GET) ===
@pokemons_bp_batalla.route('/batalla', methods=['GET'])
def batalla():
    if 'trainer' not in session and 'pokemon_seleccionado' not in session:
        return redirect(url_for('home'))

    trainer_name = session['trainer'] 
    pokemon_nombre = session['pokemon_seleccionado']
    pokemon_list = current_app.config["DATA"]
    
    #  Comprobar si ya existe una batalla en curso  
    if 'batalla_actual' in session:
        batalla_obj = session['batalla_actual']       
        
    else:
        # Si NO hay batalla en sesión, creamos una nueva
        pokemon_jugador = buscar_por_nombre(pokemon_nombre)
        
        if not pokemon_jugador:
            return redirect(url_for('pokemons_bp_lista.lista'))
        pokemon_jugador = {
        'id': pokemon_jugador.id,
        'name': pokemon_jugador.name,
        'height': pokemon_jugador.height,
        'weight': pokemon_jugador.weight,
        'stats': pokemon_jugador.stats,
        'sprites': pokemon_jugador.sprites,
        'moves': pokemon_jugador.moves,
        'types': pokemon_jugador.types
    }

        enemigo = None

        lista_enemigo = []
        for p in pokemon_list:              
            lista_enemigo.append(p)

        enemigo = random.choice(lista_enemigo)

        # --- Listas de Imágenes ---
        character_player_img = [
            "imagenes/Torrente.png", "imagenes/Gitano.png", "imagenes/Espetero.png",
            "imagenes/Cid.png", "imagenes/alain.png", "imagenes/alder.png", "imagenes/arceus.png",
            "imagenes/ash-alola.png", "imagenes/ash-capbackward.png", "imagenes/ash-hoenn.png",
            "imagenes/ash-johto.png", "imagenes/ash-kalos.png", "imagenes/ash-sinnoh.png",
            "imagenes/ash-unova.png", "imagenes/ash.png", "imagenes/ballguy.png",
            "imagenes/blue.png", "imagenes/brock-lgpe.png", "imagenes/clemont.png",
            "imagenes/cynthia-gen4.png", "imagenes/diantha.png", "imagenes/gladion.png",
            "imagenes/iniesta.png", "imagenes/iris.png", "imagenes/may-rs.png",
            "imagenes/Messi.png", "imagenes/n.png", "imagenes/oak-gen3.png",
            "imagenes/red.png", "imagenes/serena.png", "imagenes/steven.png",
            "imagenes/Xavi.png", "imagenes/dawn.png"
        ]
        enemy_player_img = [
            "imagenes/image.png", "imagenes/Espetero.png", "imagenes/Gitano.png",
            "imagenes/Torrente.png", "imagenes/Cid.png", "imagenes/Aizkolari.png",
            "imagenes/Aliados.png", "imagenes/Cayetano.png", "imagenes/Cervantes.png",
            "imagenes/Felipe_VI.png", "imagenes/ghetsis.png", "imagenes/giovanni-lgpe.png",
            "imagenes/Guiri_Playa.png", "imagenes/Guiri.png", "imagenes/Ignatius.png",
            "imagenes/lysandre.png", "imagenes/Nazareno.png", "imagenes/Reverte.png",
            "imagenes/Reyes_Cat%3Flicos.png", "imagenes/teamrocket.png", "imagenes/Torero.png",
            "imagenes/sordward-shielbert.png", "imagenes/lusamine-nihilego.png",
            "imagenes/maxie-gen6.png", "imagenes/leon.png", "imagenes/lance.png",
            "imagenes/kiawe.png", "imagenes/courtney.png", "imagenes/archie-gen6.png",
            "imagenes/cliff.png", "imagenes/xerosic.png", "imagenes/flaregrunt.png",
            "imagenes/kukui.png"
        ]
        enemy_names = {
            "imagenes/image.png": "Sergio Ramos", "imagenes/Espetero.png": "Espetero",
            "imagenes/Gitano.png": "Gitano", "imagenes/Torrente.png": "Torrente",
            "imagenes/Cid.png": "Cid", "imagenes/Aizkolari.png": "Aizkolari",
            "imagenes/Aliados.png": "Aliados", "imagenes/Cayetano.png": "Cayetano",
            "imagenes/Cervantes.png": "Cervantes", "imagenes/Felipe_VI.png": "Felipe VI",
            "imagenes/ghetsis.png": "Ghetsis", "imagenes/giovanni-lgpe.png": "Giovanni",
            "imagenes/Guiri_Playa.png": "Guiri de Playa", "imagenes/Guiri.png": "Guiri",
            "imagenes/Ignatius.png": "Ignatius", "imagenes/lysandre.png": "Lysandre",
            "imagenes/Nazareno.png": "Nazareno", "imagenes/Reverte.png": "Reverte",
            "imagenes/Reyes_Cat%3Flicos.png": "Reyes Católicos",
            "imagenes/teamrocket.png": "Team Rocket", "imagenes/Torero.png": "Torero",
            "imagenes/sordward-shielbert.png": "Sordward & Shielbert",
            "imagenes/lusamine-nihilego.png": "Lusamine & Nihilego",
            "imagenes/maxie-gen6.png": "Maxie", "imagenes/leon.png": "Leon",
            "imagenes/lance.png": "Lance", "imagenes/kiawe.png": "Kiawe",
            "imagenes/courtney.png": "Courtney", "imagenes/archie-gen6.png": "Archie",
            "imagenes/cliff.png": "Cliff", "imagenes/xerosic.png": "Xerosic",
            "imagenes/flaregrunt.png": "Flare Grunt", "imagenes/kukui.png": "Profesor Kukui"
        }

        char_img = random.choice(character_player_img)
        enemy_img = random.choice(enemy_player_img)
        enemy_name = enemy_names.get(enemy_img, "Desconocido")
        
        batalla_obj = Batalla(pokemon_jugador, enemigo, char_img, enemy_img, enemy_name, trainer_name)
        session['batalla_actual'] = batalla_obj

    return render_template("batalla.html", batalla=batalla_obj)


# === RUTA DE BATALLA (POST) ===
@pokemons_bp_batalla.route('/batalla/atacar', methods=['POST'])
def atacar():
    # Comprobar que hay una batalla en sesión
    if 'batalla_actual' not in session:
        return redirect(url_for('pokemons_bp_batalla.batalla'))
        
    # Cargar la batalla desde la sesión
    batalla_obj = session['batalla_actual']
    
    nombre_ataque = request.form.get('ataque')
    
    if nombre_ataque:

        batalla_obj.ejecutar_turno(nombre_ataque)
        
        # Guardar el estado actualizado
        session['batalla_actual'] = batalla_obj

    return redirect(url_for('pokemons_bp_batalla.batalla'))