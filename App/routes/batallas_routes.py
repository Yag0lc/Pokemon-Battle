import random
from datetime import datetime as DateTime
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from app.database.db import db
from app.models.entrenador import Entrenador
from app.models.pokemon import Pokemon_db
from app.models.batalla_db import Batalla_db, Atacar, Defender
from app.repositories.batalla_repo import obtener_batalla_entrenador
from app.repositories.pokemon_repo import buscar_por_nombre
from app.models.batalla import Batalla
from app.services.pokemon_service import listar_pokemon,buscar_por_nombre,obtener_pokemon_por_id,random_combate

pokemons_bp_batalla = Blueprint('pokemons_bp_batalla', __name__, template_folder='templates')

@pokemons_bp_batalla.route('/batalla', methods=['GET'])
def batalla():
    if 'trainer' not in session or 'pokemon_seleccionado' not in session:
        return redirect(url_for('home'))

    if 'batalla_actual' in session:
        batalla_obj = Batalla.from_dict(session['batalla_actual'])
        return render_template("batalla.html", batalla=batalla_obj)

    trainer_name = session['trainer']
    pokemon_nombre = session['pokemon_seleccionado']

    pokemon_jugador = buscar_por_nombre(pokemon_nombre)
    if not pokemon_jugador:
        return redirect(url_for('pokemons_bp_lista.lista'))

    datos_jugador = {
        'id': pokemon_jugador.id,
        'name': pokemon_jugador.name,
        'stats': pokemon_jugador.stats,
        'sprites': pokemon_jugador.sprites,
        'moves': pokemon_jugador.moves,
        'types': pokemon_jugador.types
    }
    lista_pokemons = current_app.config["DATA"]
    enemigo = random.choice(lista_pokemons)

    entrenador_actual = Entrenador.query.filter_by(nombre=trainer_name).first()
    if not entrenador_actual:
        return redirect(url_for('home'))

    entrenadores = Entrenador.query.filter(Entrenador.id != entrenador_actual.id).all()
    if entrenadores:
        rival = random.choice(entrenadores)
        enemy_name = rival.nombre
        rival_id = rival.id
    else:
        enemy_name = "Bot"
        rival_id = None

    img_jugador = random.choice(["imagenes/ash.png", "imagenes/red.png", "imagenes/dawn.png"])
    img_rival = random.choice(["imagenes/blue.png", "imagenes/giovanni-lgpe.png", "imagenes/leon.png"])

    nueva_batalla_db = Batalla_db(
        fecha=DateTime.now(),
        resultado="",
        entrenador_1=trainer_name,
        entrenador_2=enemy_name
    )

    db.session.add(nueva_batalla_db)
    db.session.commit()

    batalla_obj = Batalla(
        pokemon_jugador=datos_jugador,
        pokemon_rival=enemigo,
        character_img=img_jugador,
        enemy_img=img_rival,
        enemy_name=enemy_name,
        trainer_name=trainer_name,
        id_batalla_db=nueva_batalla_db.id
    )
    session['batalla_actual'] = batalla_obj.to_dict()
    session['rival_id'] = rival_id

    return render_template("batalla.html", batalla=batalla_obj)

@pokemons_bp_batalla.route('/batalla/atacar', methods=['POST'])
def atacar():
    if 'batalla_actual' not in session:
        return redirect(url_for('pokemons_bp_batalla.batalla'))

    batalla_obj = Batalla.from_dict(session['batalla_actual'])
    nombre_ataque = request.form.get('ataque')
    if nombre_ataque:
        batalla_obj.ejecutar_turno(nombre_ataque)

    session['batalla_actual'] = batalla_obj.to_dict()

    if batalla_obj.partida_terminada:
        guardar_resultado_db(batalla_obj)
        session.pop('batalla_actual', None)
        session.pop('rival_id', None)
        return render_template("batalla.html", batalla=batalla_obj)

    return render_template("batalla.html", batalla=batalla_obj)

def guardar_resultado_db(batalla_obj):
    entrenador_jugador = Entrenador.query.filter_by(nombre=batalla_obj.trainer_name).first()
    rival_id = session.get('rival_id')

    batalla_db = Batalla_db.query.get(batalla_obj.id_batalla_db)
    resultado = "victoria" if batalla_obj.vida_rival == 0 else "derrota"
    batalla_db.resultado = resultado

    p_jugador = batalla_obj.datos_pokemon_jugador
    p_rival = batalla_obj.datos_pokemon_rival

    verificar_guardar_pokemon(p_jugador['id'], p_jugador['name'])
    verificar_guardar_pokemon(p_rival['id'], p_rival['name'])

    db.session.add(Atacar(
        id_batalla=batalla_db.id,
        id_entrenador=entrenador_jugador.id,
        pokemon_nombre=p_jugador['name']
    ))

    if rival_id:
        db.session.add(Defender(
            id_batalla=batalla_db.id,
            id_entrenador=rival_id,
            pokemon_nombre=p_rival['name']
        ))

    db.session.commit()

def verificar_guardar_pokemon(p_id, p_name):
    if not Pokemon_db.query.get(p_id):
        db.session.add(Pokemon_db(id=p_id, name=p_name))
        db.session.commit()

@pokemons_bp_batalla.route("/batalla/historial")
@pokemons_bp_batalla.route("/historial")
def historial():
    if 'trainer' not in session:
        return redirect(url_for('home'))

    trainer_name = session['trainer']
    batallas = obtener_batalla_entrenador(trainer_name)

    return render_template("historial.html", batallas=batallas, trainer=trainer_name)

@pokemons_bp_batalla.route("/<int:batalla_id>")
def detalle_batalla(batalla_id):
    batalla = Batalla_db.query.get_or_404(batalla_id)
    return render_template("detalle_batalla.html", batalla=batalla)


@pokemons_bp_batalla.route("/eliminar/<int:batalla_id>")
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