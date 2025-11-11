from flask import Blueprint, render_template, redirect, session, current_app, url_for

pokemons_bp = Blueprint("pokemons_bp", __name__)

@pokemons_bp.route("/lista", methods=["GET"])
def lista():
    if "trainer" not in session:
        return redirect(url_for("home"))

    # CAMBIO AQUÍ: Usamos 'trainer' en lugar de 'entrenador'
    trainer = session["trainer"]
    pokemon_list = current_app.config["DATA"]

    # CAMBIO AQUÍ: Pasamos 'trainer'
    return render_template("Lista.html", trainer=trainer, pokemon=pokemon_list)


@pokemons_bp.route("/lista/<int:pokemon_id>")
def datos(pokemon_id):
    pokemon_list = current_app.config["DATA"]
    pokemon = next((poke for poke in pokemon_list if poke.get("id") == pokemon_id), None)
    
    if pokemon is None:
        return "Pokémon no encontrado", 404
    
    return render_template("Datos.html", pokemon=pokemon)