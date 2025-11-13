import random

class Batalla:
    """
    Esta clase modela y almacena el estado completo de una batalla Pokémon.
    """
    
    def __init__(self, pokemon_jugador, pokemon_rival, character_img, enemy_img, enemy_name, trainer_name):
        """
        Inicializa la batalla, seleccionando ataques y guardando estadísticas.
        """
        # --- Datos Generales ---
        self.datos_pokemon_jugador = pokemon_jugador
        self.datos_pokemon_rival = pokemon_rival
        self.character_img = character_img
        self.enemy_img = enemy_img
        self.enemy_name = enemy_name
        self.trainer_name = trainer_name # Para mostrar el nombre del jugador

        # --- Estadísticas del Jugador ---
        self.velocidad_jugador = self._get_stat(pokemon_jugador, 'speed')
        self.vida_max_jugador = self._get_stat(pokemon_jugador, 'hp')
        self.vida_jugador = self.vida_max_jugador # Vida actual empieza al máximo

        # --- Estadísticas del Rival ---
        self.velocidad_rival = self._get_stat(pokemon_rival, 'speed')
        self.vida_max_rival = self._get_stat(pokemon_rival, 'hp')
        self.vida_rival = self.vida_max_rival # Vida actual empieza al máximo

        # --- Selección de Ataques ---
        self.ataques_jugador = self._seleccionar_ataques(pokemon_jugador)
        self.ataques_rival = self._seleccionar_ataques(pokemon_rival)

        # --- Control de Estado de la Batalla ---
        self.log = [] # El log empieza vacío
        self.turno = 1
        # --- ¡ARREGLO IMPORTANTE! ---
        # Añadimos 'partida_terminada' para que exista desde el principio.
        self.partida_terminada = False


    def _get_stat(self, pokemon, stat_name):
        """
        Método auxiliar para obtener un stat específico del JSON del Pokémon.
        Busca por 'value', como en tu JSON.
        """
        for stat in pokemon.get('stats', []):
            if stat.get('name') == stat_name:
                return stat.get('value', 50) # 50 como valor por defecto
        return 50

    def _seleccionar_ataques(self, pokemon):
        """
        Método auxiliar para seleccionar 4 ataques aleatorios de la lista.
        """
        moves = pokemon.get('moves', [])
        if len(moves) <= 4:
            return moves
        return random.sample(moves, 4)

    def ejecutar_turno(self, nombre_ataque_jugador):
        """
        El método principal que procesa un turno completo de batalla.
        """
        # 1. No hacer nada si la batalla ya terminó
        if self.partida_terminada:
            return

        # 2. Encontrar el ataque que el jugador seleccionó
        ataque_jugador = next((a for a in self.ataques_jugador if a['name'] == nombre_ataque_jugador), None)
        if not ataque_jugador:
            self.log.append(f"¡{self.datos_pokemon_jugador['name'].title()} tried to use an unknown move!")
            return

        # 3. El rival elige un ataque al azar
        ataque_rival = random.choice(self.ataques_rival)

        # 4. Decidir el orden de ataque basado en la VELOCIDAD
        self.log.append(f"--- Turno {self.turno} ---")
        
        if self.velocidad_jugador >= self.velocidad_rival:
            # Primero ataca el Jugador
            self._resolver_ataque(self.datos_pokemon_jugador, self.datos_pokemon_rival, ataque_jugador)
            
            # El rival solo ataca si la batalla no ha terminado
            if not self.partida_terminada:
                self._resolver_ataque(self.datos_pokemon_rival, self.datos_pokemon_jugador, ataque_rival)
        else:
            # Primero ataca el Rival
            self._resolver_ataque(self.datos_pokemon_rival, self.datos_pokemon_jugador, ataque_rival)
            
            # El jugador solo ataca si la batalla no ha terminado
            if not self.partida_terminada:
                self._resolver_ataque(self.datos_pokemon_jugador, self.datos_pokemon_rival, ataque_jugador)
        
        self.turno += 1

    def _resolver_ataque(self, atacante, defensor, ataque):
        """
        Lógica para un solo ataque (cálculo de precisión, daño, etc.).
        """
        # Obtener nombres para el log
        nombre_atacante = atacante['name'].title()
        nombre_defensor = defensor['name'].title()
        nombre_ataque = ataque['name'].replace('-', ' ').title()

        # 1. Filtro para ataques de estado (ej. Látigo)
        power = ataque.get('power')
        if power is None or power == 0:
            self.log.append(f"¡{nombre_atacante} use {nombre_ataque}! But it had no effect!")
            return

        # 2. Comprobar Precisión (Accuracy)
        accuracy = ataque.get('accuracy', 100) # Asumir 100% si no está definido
        if accuracy is None: # A veces el JSON trae 'null'
            accuracy = 100
            
        if random.randint(1, 100) > accuracy:
            self.log.append(f"¡{nombre_atacante} use {nombre_ataque}! The attack missed!")
            return # El ataque falla, termina

        # 3. Calcular Daño (simple, usamos 'power' como daño directo)
        dano = power
        
        # 4. Aplicar daño (actualizar la vida en ESTA clase)
        if atacante['id'] == self.datos_pokemon_jugador['id']:
            # Si el atacante es el jugador, el defensor es el rival
            self.vida_rival -= dano
            if self.vida_rival < 0: self.vida_rival = 0
            vida_restante = self.vida_rival
        else:
            # Si el atacante es el rival, el defensor es el jugador
            self.vida_jugador -= dano
            if self.vida_jugador < 0: self.vida_jugador = 0
            vida_restante = self.vida_jugador
        
        # 5. Registrar la acción en el log
        self.log.append(
            f"¡{nombre_atacante} use {nombre_ataque}! "
            f"{nombre_defensor} lost {dano} HP."
        )

        # 6. Comprobar si la batalla termina (K.O.)
        if self.vida_jugador == 0 or self.vida_rival == 0:
            self.partida_terminada = True
            
            if self.vida_jugador > 0:
                ganador = self.datos_pokemon_jugador['name'].title()
                perdedor = self.datos_pokemon_rival['name'].title()
            else:
                ganador = self.datos_pokemon_rival['name'].title()
                perdedor = self.datos_pokemon_jugador['name'].title()

            self.log.append(f"¡{perdedor} has been weakened!")
            # Mensaje simplificado como pediste:
            self.log.append(f"¡{ganador} has won the battle!")