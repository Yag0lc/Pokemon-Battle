import os
import random
from flask import Flask, current_app, json, render_template, request, redirect, url_for, session
from flask_session import Session
from App.routes.pokemon_routes import pokemons_bp_lista
from App.models.batalla import Batalla
from App.routes.batallas_routes import pokemons_bp_batalla

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
app.register_blueprint(pokemons_bp_lista, url_prefix="/pokemons")
app.register_blueprint(pokemons_bp_batalla, url_prefix="/batalla")



# === RUTA PRINCIPAL ===
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entrenador = request.form.get('trainer', '').strip()
        
        if entrenador and 3 <= len(entrenador) <= 15:
            session['trainer'] = entrenador
            return redirect(url_for('pokemons_bp_lista.lista'))
        else:
            errorNombre = "El nombre del entrenador debe tener entre 3 y 15 caracteres."
            return render_template('Home.html', errorNombre=errorNombre)
    
    if 'trainer' in session:
        return redirect(url_for('pokemons_bp_lista.lista'))

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
        return redirect(url_for('pokemons_bp_batalla.batalla'))
    else:
        return redirect(url_for('pokemons_bp_lista.lista'))



# === RUTA PARA CERRAR SESIÓN ===
@app.route('/logout')
def logout():
    session.pop('trainer', None)
    session.pop('pokemon_seleccionado', None)
    session.pop('batalla_actual', None)
    return redirect(url_for('home'))


# === EJECUCIÓN ===
app.run('0.0.0.0', 8080, debug=True)