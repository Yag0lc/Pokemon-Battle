from App.database.db import db
from sqlalchemy import Column, Integer, String

class Entrenador(db.Model):
    __tablename__ = "entrenadores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    
    def __repr__(self):
        return f'<Entrenador {self.nombre}>'

