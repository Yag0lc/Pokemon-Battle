from App.models.entrenador import Entrenador
from App.database.db import db

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
    if buscarEntrenador(nombre=nombre) == None:
        return crearEntrenador(nombre= nombre, password = password)
    return None

def borrarEntrenador(entrenador):
    if buscarEntrenador(nombre=entrenador.nombre):
        db.session.delete(entrenador)
        db.session.commit()
    return None


def actualizacionEntrenador(entrenador, nuevoNombre, nuevoPassword): 
    buscarEntrenador(nombre=entrenador.nombre)
    
    return None

def autenticarEntrenador(nombre, password):
    
    entrenadores = obtenerTodoEntrenadores()

    for entrenador in entrenadores:
        if entrenador.nombre == nombre:
            if entrenador.password == password:
                return entrenador

    return None    
        