from data import db
from sqlalchemy import Column, String 

class Entrenador(db.Model):
    __tablename__ = "usuarios"
    id = Column(String, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    password = Column(String ,  nullable=False)

def crear_tablas():
    print("Creando estructura de base de datos...")
    db.create_all()
    print("Base de datos creada correctamente.")
    