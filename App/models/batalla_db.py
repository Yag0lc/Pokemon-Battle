from app.database.db import db
from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.pokemon import Pokemon


class Batalla_db(db.Model):
    __tablename__ = 'batalla'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resultado = Column(Boolean, nullable=False)
    fecha = Column(Date, nullable=False)

    atacantes = relationship(
        'Entrenador',
        secondary='atacar',
        back_populates='batallas_atacadas'
    )

    defensores = relationship(
        'Entrenador',
        secondary='defender',
        back_populates='batallas_defendidas'
    )


class Atacar(db.Model):
    __tablename__ = 'atacar'

    id_batalla = Column(
        Integer,
        ForeignKey('batalla.id', ondelete='CASCADE'),
        primary_key=True
    )

    id_entrenador = Column(
        Integer,
        ForeignKey('entrenadores.id', ondelete='RESTRICT'),
        primary_key=True
    )

    pokemon_id = Column(
        Integer,
        ForeignKey('pokemon.id'),
        nullable=False
    )


class Defender(db.Model):
    __tablename__ = 'defender'

    id_batalla = Column(
        Integer,
        ForeignKey('batalla.id', ondelete='CASCADE'),
        primary_key=True
    )

    id_entrenador = Column(
        Integer,
        ForeignKey('entrenadores.id', ondelete='RESTRICT'),
        primary_key=True
    )

    pokemon_id = Column(
        Integer,
        ForeignKey('pokemon.id'),
        nullable=False
    )
