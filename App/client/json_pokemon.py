import requests

def validar_producto(data):
    if "id" not in data or "nombre" not in data:
        return False
    return True

def adaptar_producto(data):
    return {
        "id": data["id"],
        "name": data["name"],
        "type": data["type"]
    }

def fech_pokemon_default(url):

    response = requests.get(url)
    return response.json()



#CAMBIAR https://dir.gitbook.io/dwes/unidades-didacticas/ud7-aplicaciones-web-hibridas/apis/libreria-requests URL/PARAMS
  
def get_pokemons():
    pokemons = []
    url= 'https://pokeapi.co/api/v2/pokemon/?limit=5'

    data = fech_pokemon_default(url)

    for p in data['results']:   
        urlPokemon= p['url']
        dataPokemon = fech_pokemon_default(urlPokemon)
        pokemon = adaptar_pokemon(dataPokemon)
        pokemons.append(pokemon)
        
    return pokemons





def get_pokemon_id(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


    resp = requests.get(url, timeout=10)
    data = resp.json()  

    pokemon = adaptar_pokemon(data)

    return pokemon

def get_pokemon_nombre(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"


    resp = requests.get(url, timeout=10)
    data = resp.json()  

    pokemon = adaptar_pokemon(data)

    return pokemon


    
def adaptar_pokemon(data):
    movimientos = []
    cont = 0
    for m in data["moves"]:

        url = m["move"]["url"]
        respu = requests.get(url, timeout=10)    
        moves = respu.json()

        movimiento = adaptar_moves(moves)

        movimientos.append(movimiento)

        cont=cont+1
        if cont == 3:
            break


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

    sprites = {
        "back_default": data['sprites']["back_default"],
        "back_shiny": data['sprites']["back_shiny"],
        "front_default": data['sprites']["front_default"],
        "front_shiny": data['sprites']["front_shiny"]
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
    print(get_pokemons())
    # print(get_pokemon_nombre('pikachu'))

    





    