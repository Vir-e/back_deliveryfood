from config.database import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean

class CartaModel(Base):
    __tablename__ = 'carta'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)

    
    def __init__(self, nombre=None, precio=None, id=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio



