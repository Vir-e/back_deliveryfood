from config.database import Base
from sqlalchemy import Column, Integer, String, Numeric

class ProductoModel(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255))
    stock = Column(Integer)
    precio_kg = Column(Numeric(10, 2))

    
    def __init__(self, nombre=None, precio_kg=None, id=None, stock=None):
        self.id = id
        self.nombre = nombre
        self.precio_kg = precio_kg
        self.stock = stock

