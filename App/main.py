import os
import random
from flask import Flask, current_app, json, render_template, request, redirect, url_for, session
from flask_session import Session
from app.routes.pokemon_routes import pokemons_bp_lista
from app.models.batalla import Batalla
from app.routes.batallas_routes import pokemons_bp_batalla
from app.database.db import db
from app.services.entrenador_service import comprobarEntrenador,registrarEntrenador
import logging
logging.basicConfig(level=logging.DEBUG)

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
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'pokemon.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    

db.init_app(app)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)

# === REGISTRO DEL BLUEPRINT ===

app.register_blueprint(pokemons_bp_lista, url_prefix="/pokemons")
app.register_blueprint(pokemons_bp_batalla, url_prefix="/batalla")



# === RUTA PRINCIPAL ===
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nombre = request.form.get('trainer', '').strip()
        password = request.form.get('password', '').strip()

        if nombre and 3 <= len(nombre) <= 15:
            if comprobarEntrenador(nombre,password):
                session['trainer'] = nombre
                return redirect(url_for('pokemons_bp_lista.lista'))
        else:
            return render_template('Home.html', errorNombre="El nombre debe tener entre 3 y 15 caracteres.")
    
    if 'trainer' in session:
        return redirect(url_for('pokemons_bp_lista.lista'))

    return render_template('Home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('trainer', '').strip()
        password = request.form.get('password', '').strip()

        if not (3 <= len(nombre) <= 15):
            return render_template('Register.html', errorNombre="El nombre debe tener entre 3 y 15 caracteres.")
        

        if len(password) < 3:
            return render_template('Register.html', errorNombre="La contraseña debe tener mínimo 3 caracteres.")

        entrenador = registrarEntrenador(nombre,password)
        if entrenador:
            return render_template('Home.html')


    return render_template('Register.html')

# === RUTA PARA CERRAR SESIÓN ===
@app.route('/logout')
def logout():
    session.pop('trainer', None)
    session.pop('pokemon_seleccionado', None)
    session.pop('batalla_actual', None)
    return redirect(url_for('home'))

# === Comprobar si se crean las talbas===
@app.cli.command("crear-tablas")
def crear_tablas():
    print("Creando estructura de base de datos...")
    db.drop_all()
    db.create_all()
    print("Base de datos creada correctamente.")


# === EJECUCIÓN ===
app.run('0.0.0.0', 8080, debug=True)