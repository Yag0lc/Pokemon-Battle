import requests
import random



def fech_pokemon_default(url):

    response = requests.get(url)
    return response.json()



#CAMBIAR https://dir.gitbook.io/dwes/unidades-didacticas/ud7-aplicaciones-web-hibridas/apis/libreria-requests URL/PARAMS
  
def get_pokemons(pagina):
    limit = 5
    offset = (pagina - 1) * limit
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"

    data = fech_pokemon_default(url)

    pokemons = []
    for p in data['results']:
        dataPokemon = fech_pokemon_default(p['url'])
        pokemon = adaptar_pokemon(dataPokemon)
        pokemons.append(pokemon)

    return {
        "pokemons": pokemons,
        "count": data["count"],
        "next": data["next"],
        "previous": data["previous"]
    }


def get_pokemon_battle():
    url = 'https://pokeapi.co/api/v2/pokemon/?limit=20000'
    data = fech_pokemon_default(url)
    
    # Escoger un Pokémon al azar de toda la lista
    random_pokemon = random.choice(data['results'])
    
    urlPokemon = random_pokemon['url']
    resp = requests.get(urlPokemon, timeout=10)
    dataPokemon = resp.json()
    
    pokemon = adaptar_pokemon(dataPokemon)
    return pokemon


def get_pokemon_id(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


    resp = requests.get(url, timeout=10)
    data = resp.json()  

    pokemon = adaptar_pokemon(data)

    return pokemon

def get_pokemon_nombre(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"


    resp = requests.get(url, timeout=100)
    data = resp.json()  

    pokemon = adaptar_pokemon(data)

    return pokemon


    
def adaptar_pokemon(data):
    movimientos = []

    moves_random = random.sample(
        data["moves"],
        k=min(4, len(data["moves"]))
    )

    for m in moves_random:
        url = m["move"]["url"]
        resp = requests.get(url, timeout=100)
        move_data = resp.json()

        movimiento = adaptar_moves(move_data)
        movimientos.append(movimiento)


    tipos = []
    for t in data["types"]:
        tipos.append(t["type"]["name"])

    stats = []
    for s in data["stats"]:
        stat = {
            'name': s["stat"]["name"],
            'value': s["base_stat"]
        }
        stats.append(stat)  

    default_sprite = "app/static/imagenes/zmissingno_sprite_by_retronc_dg60lg7-fullview.png"

    sprites = {
        "back_default": data['sprites']["back_default"] or default_sprite,
        "back_shiny": data['sprites']["back_shiny"] or default_sprite,
        "front_default": data['sprites']["front_default"] or default_sprite,
        "front_shiny": data['sprites']["front_shiny"] or default_sprite
    }
    

    pokemon = {
        'name' : data['name'],
        'id' : data['id'],
        'types': tipos,
        'stats': stats,
        'height': data['height'],
        'weight': data['weight'],
        'moves':movimientos,
        'sprites':sprites

    }

    return pokemon


    # ARquivo script.py

def adaptar_moves(data):
    movimiento = {
        'name': data['name'],
        "accuracy":data["accuracy"],
        'power': data['power'],
        "type":data["type"]['name']
    }
    return movimiento



def funcion_principal():
    pass

if __name__ == "__main__":
    print("Este código execútase cando o script é executado directamente.")
    funcion_principal()
    # print(get_pokemon_id(9))
    # print(get_pokemons())
    print(get_pokemon_nombre('venusaur'))

    





    