import random
from flask import json

class batalla: 
    def __init__(self,pokemon_player,pokemon_enemy,character_img,enemy_img,enemy_name):

        self.data_pokemon_player = pokemon_player
        self.data_pokemon_enemy = pokemon_enemy

        self.ataques_jugador = self.seleccionar_ataques(pokemon_player)
        self.ataques_rival = self.seleccionar_ataques(pokemon_enemy)

        self.vida_max_jugador = self._get_stat(pokemon_player, 'hp')
        self.vida_jugador = self.vida_max_jugador

        self.turno = 1
        self.log = []

        self.character_player_img = character_img
        self.enemy_player_img = enemy_img
        self.enemy_name = enemy_name

        self.vista_jugador = self.vista(pokemon_player, self.ataques_jugador)
        self.vista_rival = self.vista(pokemon_enemy, self.ataques_rival)