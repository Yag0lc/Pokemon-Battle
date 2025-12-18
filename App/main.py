import os
import sqlite3
from flask import Flask, current_app, json, render_template, request, redirect, url_for, session
from flask_session import Session
from app.routes.pokemon_routes import pokemons_bp_lista
from app.routes.batallas_routes import pokemons_bp_batalla
from app.database.db import db
from app.routes.home_routes import pokemons_bp_home
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

def sqlite_creator():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "creator": sqlite_creator
}
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    

db.init_app(app)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    app.config["DATA"] = json.load(f)

# === REGISTRO DEL BLUEPRINT ===

app.register_blueprint(pokemons_bp_lista, url_prefix="/pokemons")
app.register_blueprint(pokemons_bp_batalla, url_prefix="/batalla")
app.register_blueprint(pokemons_bp_home, url_prefix='/' )


# === Comprobar si se crean las talbas===
@app.cli.command("crear-tablas")
def crear_tablas():
    print("Creando estructura de base de datos...")
    db.drop_all()
    db.create_all()
    print("Base de datos creada correctamente.")


# === EJECUCIÓN ===
app.run('0.0.0.0', 8080, debug=True)