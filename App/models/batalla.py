import random
from app.repositories.batalla_repo import get_stat, seleccionar_ataques

class Batalla:

    def __init__(self, pokemon_jugador, pokemon_rival, character_img, enemy_img, enemy_name, trainer_name):
        self.datos_pokemon_jugador = pokemon_jugador
        self.datos_pokemon_rival = pokemon_rival

        self.character_img = character_img
        self.enemy_img = enemy_img
        self.enemy_name = enemy_name
        self.trainer_name = trainer_name

        self.vida_max_jugador = get_stat(pokemon_jugador, 'hp')
        self.vida_jugador = self.vida_max_jugador

        self.vida_max_rival = get_stat(pokemon_rival, 'hp')
        self.vida_rival = self.vida_max_rival

        self.ataques_jugador = seleccionar_ataques(pokemon_jugador)
        self.ataques_rival = seleccionar_ataques(pokemon_rival)

        self.log = []
        self.turno = 1
        self.partida_terminada = False

    def ejecutar_turno(self, nombre_ataque_jugador):
        if self.partida_terminada:
            return

        ataque_jugador = next(
            (a for a in self.ataques_jugador if a.get('name') == nombre_ataque_jugador),
            None
        )

        if not ataque_jugador:
            self.log.append("¡That attack doesn't exist!")
            return

        ataque_rival = random.choice(self.ataques_rival)

        self.resolver_ataque(self.datos_pokemon_jugador, self.datos_pokemon_rival, ataque_jugador)

        if not self.partida_terminada:
            self.resolver_ataque(self.datos_pokemon_rival, self.datos_pokemon_jugador, ataque_rival)

        self.turno += 1

    def resolver_ataque(self, atacante, defensor, ataque):
        porcentaje = random.randint(1, 100)

        if porcentaje > ataque.get('accuracy', 100):
            self.log.append(f"{atacante['name']} used {ataque['name']} but failed")
            return

        if defensor == self.datos_pokemon_rival:
            daño = int(self.vida_max_rival * ataque.get('power', 50) / 100)
            daño = min(daño, self.vida_rival)
            self.vida_rival -= daño
            hp_restante = self.vida_rival
        else:
            daño = int(self.vida_max_jugador * ataque.get('power', 50) / 100)
            daño = min(daño, self.vida_jugador)
            self.vida_jugador -= daño
            hp_restante = self.vida_jugador

        self.log.append(f"{atacante['name']} used {ataque['name']}")

        if hp_restante == 0:
            self.log.append(f"¡{defensor['name']} has been weakened!")
            self.log.append(f"¡{atacante['name']} has won the battle!")
            self.partida_terminada = True
