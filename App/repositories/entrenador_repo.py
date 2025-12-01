from app.models.entrenador import Entrenador
from app.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


def crearEntrenador(nombre, password):
    hash_password = generate_password_hash(password)
    entrenador_nuevo = Entrenador(nombre=nombre, password=hash_password)
    db.session.add(entrenador_nuevo)
    db.session.commit()
    return entrenador_nuevo


def buscarEntrenador(nombre):
    return Entrenador.query.filter_by(nombre=nombre).first()


def obtenerTodoEntrenadores():
    return Entrenador.query.all()

def borrarEntrenador(entrenador):
    db.session.delete(entrenador)
    db.session.commit()
    return None


def actualizacionEntrenador(entrenador, nuevoNombre, nuevoPassword):
    entrenador.nombre = nuevoNombre
    entrenador.password = generate_password_hash(nuevoPassword)
    db.session.commit()
    return entrenador


def comprobarPassword(entrenador, password):
    return check_password_hash(entrenador.password, password)


def autenticarUsuario(nombre, password):
    entrenador = buscarEntrenador(nombre)

    if entrenador and comprobarPassword(entrenador, password):
        return entrenador   # Login correcto

    return None             # Credenciales inválidas
