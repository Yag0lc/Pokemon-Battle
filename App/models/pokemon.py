from app.database.db import db
from sqlalchemy import Column, Integer, String

class Pokemon_db(db.Model):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)


class Pokemon:
   def __init__(self,id,name,height,weight,stats,sprites,moves,types):
      self.height = height
      self.id = id
      self.name = name
      self.weight = weight
      self.stats = stats
      self.sprites = sprites
      self.moves = moves
      self.types = types

