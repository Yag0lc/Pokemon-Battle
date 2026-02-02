from app.database.db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Entrenador(db.Model):
    __tablename__ = "entrenadores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    win = Column(Integer, default=0, nullable=False)
    defeat = Column(Integer, default=0, nullable=False)


    batallas_atacadas = relationship(
        'Batalla_db',
        secondary='atacar',
        viewonly=True
    )

    batallas_defendidas = relationship(
        'Batalla_db',
        secondary='defender',
        viewonly=True
    )

    def __repr__(self):
        return f'<Entrenador {self.nombre}>'
