from config.database import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean

class Carta(Base):
    __tablename__ = 'carta'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    sin_gluten = Column(Boolean, nullable=False, default=False)
    sin_huevo = Column(Boolean, nullable=False, default=False)
    vegano = Column(Boolean, nullable=False, default=False)
    
    def __init__(self, nombre=None, precio=None, sin_gluten=False, sin_huevo=False, vegano=False, id=None):
        if id:
            self.id = id
        self.nombre = nombre
        self.precio = precio
        self.sin_gluten = sin_gluten
        self.sin_huevo = sin_huevo
        self.vegano = vegano