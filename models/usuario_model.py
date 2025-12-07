from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class UsuarioModel(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellidos = Column(String(100))
    username = Column(String(100))
    password = Column(String(250))
    email = Column(String(250))
    admin =  Column(Boolean)


    # def __init__(self, id=None, nombre=None, apellidos=None, username=None, password=None, email=None, admin=None):
    #     self.id = id
    #     self.nombre = nombre
    #     self.apellidos = apellidos
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.admin = admin