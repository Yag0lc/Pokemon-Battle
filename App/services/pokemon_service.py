import repositories.pokemon_repo as pokemon_repo


def listar_pokemon():
     return pokemon_repo.obtener_pokemons()

def  obtener_pokemon_por_id(id):

      if id < 0 or id is None: 
          "retrurn None"


      return pokemon_repo.buscar_por_id(id)
