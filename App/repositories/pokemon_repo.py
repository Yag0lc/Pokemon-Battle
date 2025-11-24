from flask import json
from App.models.pokemon import Pokemon 


DATA_PATH = "data/pokemon.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    _POKEMONS = json.load(f)
    

def  obtener_pokemons():
    pokemons = []
    for p in _POKEMONS: 
           pokemon = Pokemon(**p) 
           pokemons.append(pokemon)
    return pokemons

def buscar_por_id(id):
    pokemons= obtener_pokemons()
    pokemon_a_buscar = None
    for p in pokemons:
         if p.id == id:
            pokemon_a_buscar = p
            break
    return pokemon_a_buscar

def buscar_por_nombre(nombre):
    pokemons = obtener_pokemons()
    pokemon_a_buscar = None
    for p in pokemons:
         if p.name.lower() == nombre.lower():
            pokemon_a_buscar = p
            break
    return pokemon_a_buscar