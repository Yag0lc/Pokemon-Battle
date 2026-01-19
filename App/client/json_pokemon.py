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


product = []
for url in urls:
    data = fech_pokemon_default(url)
    print(data['id'])
    product.append(data)


def get_pokemon_id(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    try:
        resp = requests.get(url, timeout=10)
        data = fech_pokemon_default(url)
        print(data['name'])
        return resp.json()
        
    except:
        return None
    



    # ARquivo script.py

def funcion_principal():
    pass

if __name__ == "__main__":
    print("Este código execútase cando o script é executado directamente.")
    funcion_principal()
    get_pokemon_id(9)

    



    