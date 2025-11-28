from app.models.entrenador import Entrenador
from app.database.db import db

def crearEntrenador(nombre, password):
    entrenador_nuevo = Entrenador(nombre=nombre, password=password)
    db.session.add(entrenador_nuevo)
    db.session.commit()
    return entrenador_nuevo

def buscarEntrenador(nombre):
    entrenador_encontrado = Entrenador.query.filter_by(nombre=nombre).first()
    if (entrenador_encontrado):
        return entrenador_encontrado        
    return None

def obtenerTodoEntrenadores():
    return Entrenador.query.all() 


def reguistrarEntrenador(nombre, password):
    if buscarEntrenador(nombre=nombre) is None:
        return crearEntrenador(nombre= nombre, password = password)
    return None

def borrarEntrenador(entrenador):
    if buscarEntrenador(nombre=entrenador.nombre):
        db.session.delete(entrenador)
        db.session.commit()
    return None


def actualizacionEntrenador(entrenador, nuevoNombre, nuevoPassword):
    entrenador.nombre = nuevoNombre
    entrenador.password = nuevoPassword
    db.session.commit()
    return entrenador       


def autenticarEntrenador(nombre, password):
    
    entrenadores = obtenerTodoEntrenadores()

    for entrenador in entrenadores:
        if entrenador.nombre == nombre:
            if entrenador.password == password:
                return entrenador

    return None    
        