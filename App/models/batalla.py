import random


class Batalla:


    def __init__(self, pokemon_jugador, pokemon_rival, character_img, enemy_img, enemy_name, trainer_name):
       
        # player
        self.datos_pokemon_jugador = pokemon_jugador
        self.character_img = character_img
        self.trainer_name = trainer_name
        self.vida_max_jugador = self._get_stat(pokemon_jugador, 'hp')
        self.vida_jugador = self.vida_max_jugador
        self.ataques_jugador = self._seleccionar_ataques(pokemon_jugador)


        # enemy
        self.datos_pokemon_rival = pokemon_rival
        self.enemy_img = enemy_img
        self.enemy_name = enemy_name
        self.vida_max_rival = self._get_stat(pokemon_rival, 'hp')
        self.vida_rival = self.vida_max_rival
        self.ataques_rival = self._seleccionar_ataques(pokemon_rival)


        self.log = []


        self.turno = 1


        self.partida_terminada = False


    def _get_stat(self, pokemon, stat_name):


        for stat in pokemon.get('stats', []):
            if stat.get('name') == stat_name:
                return stat.get('value',100)
        return


    def _seleccionar_ataques(self, pokemon):


        moves = pokemon.get('moves', [])
        if len(moves) <= 4:
            return moves
        return random.sample(moves, 4)


    def ejecutar_turno(self, nombre_ataque_jugador):
       
        if self.partida_terminada:
            return
       
        ataque_jugador = None
       
        for atack in self.ataques_jugador:
            if atack.get('name') == nombre_ataque_jugador:
                ataque_jugador = atack
                break        
       
        if ataque_jugador is None:
            self.log.append("¡That atack doesn't exist!")
            return
   
        ataque_rival = random.choice(self.ataques_rival)
         
        self.resolver_ataque(self.datos_pokemon_jugador, self.datos_pokemon_rival, ataque_jugador)
       
        if not self.partida_terminada:
            self.resolver_ataque(self.datos_pokemon_rival, self.datos_pokemon_jugador, ataque_rival)


        self.turno += 1


    def resolver_ataque(self, atacante, defensor, ataque):
        porcentaje = random.randint(1, 100)
        if porcentaje > ataque.get('accuracy', 100):
            self.log.append(f"{atacante['name']} used {ataque['name']} but failed ")
            return

        if defensor == self.datos_pokemon_rival:
            daño = int(self.vida_max_rival * ataque.get('power', 50) / 100)
            hp_restante = self.vida_rival
        else:
            daño = int(self.vida_max_jugador * ataque.get('power', 50) / 100)
            hp_restante = self.vida_jugador

        daño = min(daño, hp_restante)

        if defensor == self.datos_pokemon_rival:
            self.vida_rival -= daño
            hp_restante = self.vida_rival
        else:
            self.vida_jugador -= daño
            hp_restante = self.vida_jugador

        self.log.append(f"{atacante['name']} used {ataque['name']}>")

        if hp_restante == 0:
            self.log.append(f"¡{defensor['name']} has been weakened!")
            self.log.append(f"¡{atacante['name']} has won the battle!")
            self.partida_terminada = True





