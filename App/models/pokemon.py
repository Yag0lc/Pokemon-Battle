from app.database.db import db
from sqlalchemy import Column, Integer, String


class Pokemon_db(db.Model):
   __tablename__ = 'pokemon'
   id = Column(Integer, primary_key=True, autoincrement=False)
   name = Column(String(50), nullable=False)
   # height = Column(Integer, nullable=False)
   # weight = Column(Integer, nullable=False)
   # stats = Column(String(500), nullable=False)
   # sprites = Column(String(500), nullable=False)
   # moves = Column(String(1000), nullable=False)
   # types = Column(String(100), nullable=False)

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

