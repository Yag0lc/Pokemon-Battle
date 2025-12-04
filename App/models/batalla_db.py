from app.database.db import db
from sqlalchemy import Column, Integer, String, Boolean,Date,ForeignKey
from sqlalchemy.orm import relationship
from pokemon import Pokemon

class Batalla_db(db.Model):

    __tablename__ = 'Batalla'

    id = Column(Integer,primary_key=True, autoincrement=True)
    resultado = Column(Boolean, nullable=False)
    fecha = Column(Date,nullable=False)

    atacante = relationship(
        'Entrenador',
        secondary='Atacar',
        back_populates='batallas'
    )

    defensor = relationship(
        'Entrenador',
        secondary='Defender',
        back_populates='batallas'
    )




class Atacar(db.Model):
    __tablename__='Atacar'

    id_batalla = Column(Integer,ForeignKey('Batalla.id', ondelete='CASCADE'), primary_key=True)
    id_entrenador = Column(Integer,ForeignKey('entrenadores.id', ondelete='RESTRICT'), primary_key=True)
    
    pokemon1 = Column(Integer,Pokemon.id)

    batalla = relationship("Batalla_db", back_populates="atacante")





class Defender(db.Model):
    __tablename__='Defender'

    id_batalla = Column(Integer,ForeignKey('Batalla.id', ondelete='RESTRICT'), primary_key=True)
    id_entrenador = Column(Integer,ForeignKey('entrenadores.id', ondelete='RESTRICT'), primary_key=True)

    batalla = relationship("Batalla_db", back_populates="atacante")