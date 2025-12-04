from datetime import date, datetime
from app.database.db import db
from app.models.batalla_db import Batalla_db


def get_stat(pokemon, nombre):

    for stat in pokemon.get('stats', []):
        if stat.get('name') == nombre:
            return stat.get('value', 50) # 50 como valor por defecto
    return 50



def crear_batalla(resultado):
    
    batalla_nueva = Batalla_db(resultado=resultado, fecha=datetime.now)
    db.session.add(batalla_nueva)
    db.session.commit()
    return batalla_nueva