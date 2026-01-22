import app.repositories.pokemon_repo as pokemon_repo
import app.client.json_pokemon as poke_api



def listar_pokemon():
     return poke_api.get_pokemons()

# def listar_pokemon():
#      return pokemon_repo.obtener_pokemons()

def  obtener_pokemon_por_id(id):
    if id< 0 or id is None:
        return None

    return poke_api.get_pokemon_id(id)

# def  obtener_pokemon_por_id(id):
#       if id < 0 or id is None: 
#           return None

#       return pokemon_repo.buscar_por_id(id)


def buscar_por_nombre(nombre):
    if nombre is None:
        return None
    
    return poke_api.get_pokemon_nombre(nombre)

# def buscar_por_nombre(nombre):
    
#     if nombre is None:
#         return None

#     return pokemon_repo.buscar_por_nombre(nombre)





