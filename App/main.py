import os
import random
from flask import Flask, current_app, json, render_template, request, redirect, url_for, session
from flask_session import Session
from App.routes.pokemon_routes import pokemons_bp

app = Flask(__name__)

# === CONFIGURACIÓN DE SESIÓN ===
app.config['SECRET_KEY'] = "Pokemon-Battle"
app.config['SESSION_TYPE'] = 'filesystem'  # Guarda sesiones en archivos
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Firma las cookies para mayor seguridad

# Inicializar Flask-Session
Session(app)

# === CARGA DE DATOS ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "pokemon.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)

# === REGISTRO DEL BLUEPRINT ===
app.register_blueprint(pokemons_bp, url_prefix="/pokemons")


# === RUTA PRINCIPAL ===
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entrenador = request.form.get('trainer', '').strip()
        
        # Validación del nombre del entrenador
        if entrenador and 3 <= len(entrenador) <= 15:
            # Guardar en sesión
            session['trainer'] = entrenador
            return redirect(url_for('pokemons_bp.lista'))
        else:
            errorNombre = "El nombre del entrenador debe tener entre 3 y 15 caracteres."
            return render_template('Home.html', errorNombre=errorNombre)
    
    return render_template('Home.html')


@app.route('/seleccionar_pokemon', methods=['POST'])
def guardar_pokemon():
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    pokemon_nombre = request.form.get('pokemon', '').strip()
    
    if pokemon_nombre:
        # Guardar en sesión
        session['pokemon_seleccionado'] = pokemon_nombre
        return redirect(url_for('batalla'))  # ahora la URL no tendrá el nombre
    else:
        return redirect(url_for('pokemons_bp.lista'))


# === RUTA DE BATALLA ===
@app.route('/batalla', methods=['GET'])
def batalla():
    if 'trainer' not in session or 'pokemon_seleccionado' not in session:
        return redirect(url_for('pokemons_bp.lista'))

    nombre = session['pokemon_seleccionado']
    trainer = session['trainer']
    pokemon_list = current_app.config["DATA"]
    
    pokemon = next((p for p in pokemon_list if p['name'].lower() == nombre.lower()), None)
    
    if not pokemon:
        errorCombate = f"No se encontró un Pokémon con el nombre '{nombre}'."
        return render_template("Lista.html", pokemon=pokemon_list, trainer=trainer, errorCombate=errorCombate)
    
    # … resto de tu código de batalla …



    pokemon = next((poke for poke in pokemon_list if poke.get("name").lower() == nombre.lower()), None)

    if pokemon:
        enemigo = random.choice(pokemon_list)

        pokemon_moves = pokemon.copy()
        pokemon_moves["moves"] = random.sample(pokemon["moves"], min(4, len(pokemon["moves"])))

        enemigo_con_moves = enemigo.copy()
        enemigo_con_moves["moves"] = random.sample(enemigo["moves"], min(4, len(enemigo["moves"])))

        # Imágenes del jugador y del enemigo
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

        character_player = random.choice(character_player_img)
        enemy_player = random.choice(enemy_player_img)
        enemy_name = enemy_names.get(enemy_player, "Desconocido")

        return render_template(
            "batalla.html",
            pokemon=pokemon_moves,
            trainer=trainer,
            enemigo=enemigo_con_moves,
            character_player=character_player,
            enemy_player=enemy_player,
            enemy_name=enemy_name
        )
    else:
        errorCombate = f"No se encontró un Pokémon con el nombre '{nombre}'."
        return render_template("Lista.html", pokemon=pokemon_list, trainer=trainer, errorCombate=errorCombate)


# === RUTA PARA CERRAR SESIÓN (OPCIONAL) ===
@app.route('/logout')
def logout():
    session.pop('trainer', None)
    return redirect(url_for('home'))


# === EJECUCIÓN ===
if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)