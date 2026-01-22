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

urls = [
    "https://pokeapi.co/api/v2/pokemon/3/",
    "https://pokeapi.co/api/v2/pokemon/6/",
    "https://pokeapi.co/api/v2/pokemon/9/",
    "https://pokeapi.co/api/v2/pokemon/181/",
    "https://pokeapi.co/api/v2/pokemon/25/"

]

def get_pokemons():
    pokemons = []
    for url in urls:
        data = fech_pokemon_default(url)
        pokemon = adaptar_pokemon(data)
        pokemons.append(pokemon)

    return pokemons



def get_pokemon_id(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()  

        pokemon = adaptar_pokemon(data)

        return pokemon

    except:
        print("Error")
        return None

    
def adaptar_pokemon(data):
    movimientos = []
    for m in data["moves"]:
        url = m["move"]["url"]
    

    tipos = []
    for t in data["types"]:
        tipos.append(t["type"]["name"])

    stats = []
    for s in data["stats"]:
        stat = {
            'nombre': s["stat"]["name"],
            'base_stat': s["base_stat"]
        }
        stats.append(stat)

    pokemon = {
        'nombre' : data['name'],
        'id' : data['id'],
        'tipo': tipos,
        'stats': stats,
        'height': data['height'],
        'weight': data['weight'],
        'move':movimientos

        

    }

    return pokemon


    # ARquivo script.py

def funcion_principal():
    pass

if __name__ == "__main__":
    print("Este código execútase cando o script é executado directamente.")
    funcion_principal()
    print(get_pokemon_id(9))
    # print(get_pokemons())

    





    