from datetime import date, datetime
from app.database.db import db
from app.models.batalla_db import Batalla_db
import random

from app.models.pokemon import Pokemon_db

def get_stat(pokemon, nombre):
    for stat in pokemon['stats']:
        if stat.get('name') == nombre:
            return stat.get('value', 50)
    return 50

def seleccionar_ataques(pokemon):
    moves = pokemon.get('moves', [])
    if len(moves) <= 4:
        return moves
    return random.sample(moves, 4)
 


def crear_batalla(resultado, atacante, defensor):
    
    batalla_nueva = Batalla_db(resultado=resultado, atacante=atacante, defensor=defensor, fecha=datetime.now)
    db.session.add(batalla_nueva)
    db.session.commit()
    return batalla_nueva

def obtener_batalla_id(id):
        return Batalla_db.query.filter_by(id=id).first()


def obtener_batalla_entrenador(nombre_entrenador):    
    return Batalla_db.query.filter_by(entrenador_1=nombre_entrenador).all()

def eliminar_batalla(batalla):
    if db.session.delete(batalla):
        db.session.commit()
        return True
    return None
