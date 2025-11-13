🏆 Pokémon Arena 🏆 

Autores:

Hugo Rey Zas

Yago López Carracedo

----------- Descripción general -----------

Pokémon Arena es una aplicación web que simula combates Pokémon 1 vs 1.
Permite explorar una lista de Pokémon, consultar sus detalles y enfrentarlos en una batalla dinámica dentro de la arena.

----------- Tecnologías utilizadas -----------

Frontend: HTML5, CSS3

Backend: Python 3 con Flask

----------- Flujo de interacción -----------

- Home (Inicio)

Página principal de la aplicación.

Presenta el título del proyecto y Da la bienvenida al usuario e introduce brevemente la dinámica del juego

Incluye un formulario donde escribes tu nombre de entrenador y al darle al boton pasas a la lista para seleccionar al pokemon


- Lista de Pokémon

Muestra todos los Pokémon disponibles para seleccionar.

Cada Pokémon aparece con su nombre, tipo e imagen.

Al hacer clic en un Pokémon, se accede a su vista de detalles.

Incluye un formualrio donde escribes el nombre del pokemon seleccionado y te lleva directamente a la batalla

- Detalles del Pokémon

Muestra información detallada del Pokémon seleccionado:

Nombre

Tipo

Estadísticas (vida, ataque, defensa, velocidad)

sprite



- Batalla

La arena donde se enfrentan los Pokémon seleccionados.

Muestra las barras de vida, los nombres y las imágenes de ambos.

El jugador puede atacar o defender, y el sistema calcula el resultado del turno.

El combate continúa hasta que uno de los Pokémon se queda sin vida.

Al finalizar, se muestra el ganador y la opción de volver al la lista.