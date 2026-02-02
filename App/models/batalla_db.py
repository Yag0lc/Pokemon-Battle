from app.database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

class Atacar(db.Model):
    __tablename__ = 'atacar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_batalla = Column(Integer, ForeignKey('batallas.id'))
    id_entrenador = Column(Integer, ForeignKey('entrenadores.id'))
    pokemon_nombre = Column(String(50))


class Defender(db.Model):
    __tablename__ = 'defender'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_batalla = Column(Integer, ForeignKey('batallas.id'))
    id_entrenador = Column(Integer, ForeignKey('entrenadores.id'))
    pokemon_nombre = Column(String(50))


class Batalla_db(db.Model):
    __tablename__ = 'batallas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    resultado = Column(String(20))
    entrenador_1 = Column(String(50))
    entrenador_2 = Column(String(50))
