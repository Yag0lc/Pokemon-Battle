def get_stat(pokemon, nombre):

    for stat in pokemon.get('stats', []):
        if stat.get('name') == nombre:
            return stat.get('value', 50) # 50 como valor por defecto
    return 50
