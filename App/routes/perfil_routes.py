import random
from datetime import datetime as DateTime
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from app.database.db import db
from app.models.entrenador import Entrenador
from app.models.pokemon import Pokemon_db
from app.models.batalla_db import Batalla_db, Atacar, Defender
from app.repositories.batalla_repo import obtener_batalla_entrenador
# from app.repositories.pokemon_repo import buscar_por_nombre
from app.models.batalla import Batalla
from app.services.pokemon_service import listar_pokemon,buscar_por_nombre,obtener_pokemon_por_id,random_combate




pokemons_bp_perfil = Blueprint('pokemons_bp_perfil', __name__, template_folder='templates')


@pokemons_bp_perfil.route('/historial', methods=['GET', 'POST'])
def profile():
    if 'trainer' not in session:
        return redirect(url_for('home'))
    trainer = session['trainer']
    pokemon_profile = current_app.config["DATA"]

    from app.repositories.batalla_repo import obtener_batalla_entrenador
    batallas = obtener_batalla_entrenador(trainer)

    lista_batallas = []
    for b in batallas:
        lista_batallas.append({
            'id': b.id,
            'fecha': b.fecha,
            'entrenador_1': b.entrenador_1,
            'entrenador_2': b.entrenador_2,
            'resultado': b.resultado
        })

    return render_template(
        'historial.html',
        pokemon=pokemon_profile,
        trainer=trainer,
        batallas=lista_batallas
    )





@pokemons_bp_perfil.route("/historial")
def historial():
    if 'trainer' not in session:
        return redirect(url_for('home'))

    trainer_name = session['trainer']
    batallas = obtener_batalla_entrenador(trainer_name)

    return render_template("historial.html", batallas=batallas, trainer=trainer_name)

@pokemons_bp_perfil.route("/<int:batalla_id>")
def detalle_batalla(batalla_id):
    batalla = Batalla_db.query.get_or_404(batalla_id)
    return render_template("detalle_batalla.html", batalla=batalla)


@pokemons_bp_perfil.route("/eliminar/<int:batalla_id>")
def eliminar_batalla(batalla_id):
    if 'trainer' not in session:
        return redirect(url_for('home'))

    batalla = Batalla_db.query.get_or_404(batalla_id)

    if batalla.entrenador_1 == session['trainer']:
        Atacar.query.filter_by(id_batalla=batalla.id).delete()
        Defender.query.filter_by(id_batalla=batalla.id).delete()
        
        db.session.delete(batalla)
        db.session.commit()

    return redirect(url_for("pokemons_bp_batalla.historial"))