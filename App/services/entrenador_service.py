import app.repositories.entrenador_repo as entrenador_repo

def registrarEntrenador(nombre, password):
    if entrenador_repo.buscarEntrenador(nombre) is None:
        return entrenador_repo.crearEntrenador(nombre, password)
    return None

def comprobarEntrenador(nombre,password):
    return entrenador_repo.autenticarUsuario(nombre=nombre, password=password)
