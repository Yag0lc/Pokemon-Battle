from flask import json


DATA_PATH = "data/pokemon.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    _POKEMONS = json.load(f)
    

def  obtener_pokemons():
    pokemons = []
    for p in _POKEMONS: 
           pokemon = pokemon(**p) 
           pokemons.append(pokemon)
    return pokemons

def buscar_por_id():
    pokemons= obtener_pokemons()
    pokemon_a_buscar = None
    for p in pokemons:
         if p["id"] == id:
            pokemon_a_buscar = p
            break
    return pokemon_a_buscar
