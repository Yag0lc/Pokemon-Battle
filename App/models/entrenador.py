from app.database.db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Entrenador(db.Model):
    __tablename__ = "entrenadores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    batallas_atacadas = relationship(
        'Batalla_db',
        secondary='atacar',
        back_populates='atacantes'
    )

    batallas_defendidas = relationship(
        'Batalla_db',
        secondary='defender',
        back_populates='defensores'
    )
    
    def __repr__(self):
        return f'<Entrenador {self.nombre}>'

