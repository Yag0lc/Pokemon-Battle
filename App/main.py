import os
import random
from flask import Flask, current_app, json, render_template, request, redirect, url_for, session
from flask_session import Session
from App.routes.pokemon_routes import pokemons_bp
from App.models.batalla import Batalla

app = Flask(__name__)

# === CONFIGURACIÓN DE SESIÓN ===
app.config['SECRET_KEY'] = "Pokemon-Battle"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# === CARGA DE DATOS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "pokemon.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)

# === REGISTRO DEL BLUEPRINT ===
app.register_blueprint(pokemons_bp, url_prefix="/pokemons")


# === RUTA PRINCIPAL ===
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entrenador = request.form.get('trainer', '').strip()
        
        if entrenador and 3 <= len(entrenador) <= 15:
            session['trainer'] = entrenador
            return redirect(url_for('pokemons_bp.lista'))
        else:
            errorNombre = "El nombre del entrenador debe tener entre 3 y 15 caracteres."
            return render_template('Home.html', errorNombre=errorNombre)
    
    if 'trainer' in session:
        return redirect(url_for('pokemons_bp.lista'))

    return render_template('Home.html')


@app.route('/seleccionar_pokemon', methods=['POST'])
def guardar_pokemon():
    if 'trainer' not in session:
        return redirect(url_for('home'))
    
    pokemon_nombre = request.form.get('pokemon', '').strip()
    
    if pokemon_nombre:
        if session.get('pokemon_seleccionado') != pokemon_nombre:
            session.pop('batalla_actual', None) 
            
        session['pokemon_seleccionado'] = pokemon_nombre
        return redirect(url_for('batalla'))
    else:
        return redirect(url_for('pokemons_bp.lista'))


# === RUTA DE BATALLA (GET) ===
@app.route('/batalla', methods=['GET'])
def batalla():
    #  Comprobar que tenemos todo para estar aquí
    if 'trainer' not in session or 'pokemon_seleccionado' not in session:
        return redirect(url_for('home'))

    # Recuperar datos de la sesión
    trainer_name = session['trainer']
    pokemon_nombre = session['pokemon_seleccionado']
    pokemon_list = current_app.config["DATA"]
    
    #  Comprobar si ya existe una batalla en curso
    if 'batalla_actual' in session:
        batalla_obj = session['batalla_actual']
        
        #  Asegurar compatibilidad con objetos antiguos
        if not hasattr(batalla_obj, 'partida_terminada'):
            batalla_obj.partida_terminada = False
            session['batalla_actual'] = batalla_obj
        
        # Comprobar que la batalla en sesión es del pokémon correcto
        if batalla_obj.datos_pokemon_jugador['name'].lower() != pokemon_nombre.lower():
            session.pop('batalla_actual', None)
            return redirect(url_for('batalla'))
        
    else:
        # Si NO hay batalla en sesión, creamos una nueva
        pokemon_jugador = next((p for p in pokemon_list if p['name'].lower() == pokemon_nombre.lower()), None)
        
        if not pokemon_jugador:
            return redirect(url_for('pokemons_bp.lista'))

        enemigo = random.choice([p for p in pokemon_list if p['id'] != pokemon_jugador['id']])

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

    # Renderizar la plantilla
    return render_template("batalla.html", batalla=batalla_obj)


# === RUTA DE BATALLA (POST) ===
@app.route('/batalla/atacar', methods=['POST'])
def atacar():
    # Comprobar que hay una batalla en sesión
    if 'batalla_actual' not in session:
        return redirect(url_for('batalla'))
        
    # Cargar la batalla desde la sesión
    batalla_obj = session['batalla_actual']
    
    # Obtener el ataque del formulario
    nombre_ataque = request.form.get('ataque')
    
    if nombre_ataque:
        # Ejecutar el turno
        batalla_obj.ejecutar_turno(nombre_ataque)
        
        # Guardar el estado actualizado
        session['batalla_actual'] = batalla_obj

    return redirect(url_for('batalla'))


# === RUTA PARA CERRAR SESIÓN ===
@app.route('/logout')
def logout():
    session.pop('trainer', None)
    session.pop('pokemon_seleccionado', None)
    session.pop('batalla_actual', None)
    return redirect(url_for('home'))


# === EJECUCIÓN ===
app.run('0.0.0.0', 8080, debug=True)