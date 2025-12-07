# infrastructure/repositories/usuario_repository.py (ACTUALIZADO)
from models.usuario_model import UsuarioModel
from infrastructure.datamappers.schemas.usuario_schema import UsuarioSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session # Añadimos el tipo de dato

class UsuarioRepository:
    """
    Repositorio para interactuar con la tabla de usuarios.
    La sesión de DB (db) es inyectada en el constructor.
    """
    # ⚠️ Acepta la sesión de DB (db) como dependencia
    def __init__(self, db: Session): 
        self.db = db
        # self.usuario_schema = UsuarioSchema() # Se puede mover la serialización al servicio

    # Eliminamos _get_session()

    def get_usuarios(self):
        try:
            usuarios = self.db.query(UsuarioModel).all()
            for usuario in usuarios:
                self.db.expunge(usuario) 
            return usuarios
        except SQLAlchemyError as e:
            print(f"Error al obtener usuarios: {e}")
            self.db.rollback()
            return []

    # ... otros métodos ...

    def create_usuario(self, usuario_model):
        print("|USER|REPOSITORY|CREATE", usuario_model)
        try:
            self.db.add(usuario_model)
            self.db.commit()
            self.db.refresh(usuario_model)
            self.db.expunge(usuario_model)
            return usuario_model
        except SQLAlchemyError as e:
            print(f"Error al crear un usuario: {e}")
            self.db.rollback()
            return None

    def update_usuario(self, usuario_model):
        print("USER|REPOSITORY|UPDATE|",usuario_model)
        usuario_schema = UsuarioSchema() # Instanciar aquí si se necesita serializar el resultado
        try:
            usuario_existente = self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_model.id).first()
            
            if not usuario_existente:
                return None
            
            # Asignación de atributos... (Mantenido igual)
            usuario_existente.nombre = usuario_model.nombre
            usuario_existente.apellidos = usuario_model.apellidos
            usuario_existente.username = usuario_model.username
            usuario_existente.password = usuario_model.password
            usuario_existente.email = usuario_model.email
            usuario_existente.admin = usuario_model.admin

            self.db.commit()

            resultado = usuario_schema.dump(usuario_existente) 
            self.db.expunge(usuario_existente) # Opcional si se serializó
            print("Resultado del repo:", resultado)

            return resultado
            
        except SQLAlchemyError as e:
            print(f"Error al actualizar un usuario: {e}")
            self.db.rollback()
            return None

    def delete_usuario(self, id_usuario):
        try:
            usuario_model = self.db.query(UsuarioModel).filter(UsuarioModel.id == id_usuario).first()
            if not usuario_model:
                return False
            self.db.delete(usuario_model)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error al eliminar un usuario: {e}")
            self.db.rollback()
            return False