# application/services/usuario_service.py (ACTUALIZADO)
# No necesitamos importar UsuarioRepository si se inyecta

from infrastructure.datamappers.schemas.usuario_schema import UsuarioSchema
from models.usuario_model import UsuarioModel
# Si usas tipado, puedes añadir un tipo abstracto/Protocol
# from typing import Protocol # Opcional si quieres abstracción

class UsuarioService:
    # ⚠️ Acepta el repositorio y los esquemas como dependencias
    def __init__(self, usuario_repository, schema: UsuarioSchema, schema_list: UsuarioSchema):
        self.usuario_repository = usuario_repository
        self.schema = schema
        self.schema_list = schema_list

    def get_usuarios(self):
        try:
            usuarios_model = self.usuario_repository.get_usuarios()
            return self.schema_list.dump(usuarios_model)
        except Exception as e:
            print(f"Error en el get_usuarios del servicio, {e}")
            return []

    # ... resto de los métodos (create, update, delete) se mantienen iguales, 
    # usando self.usuario_repository.
    
    def create_usuario(self, usuario_data):
        print("USER|SERVICE|CREAte", usuario_data)
        usuario_model = UsuarioModel(
            nombre=usuario_data['nombre'],
            apellidos=usuario_data['apellidos'],
            username=usuario_data['username'],
            password=usuario_data['password'],
            email=usuario_data['email'],
            admin=usuario_data['admin']
        )
        usuario_creado = self.usuario_repository.create_usuario(usuario_model)
        if usuario_creado:
            return self.schema.dump(usuario_creado)
        return None

    def update_usuario(self, id, usuario_data):
        print("USUARIO|SERVICE|UPDATE|", usuario_data)
        usuario_model = UsuarioModel(
            id=id,
            nombre=usuario_data['nombre'],
            apellidos=usuario_data['apellidos'],
            username=usuario_data['username'],
            password=usuario_data['password'],
            email=usuario_data['email'],
            admin=usuario_data['admin']
        )
        # El repositorio ya devuelve el DTO/dict serializado en la versión actualizada
        usuario_actualizado = self.usuario_repository.update_usuario(usuario_model)
        if usuario_actualizado:
            # Aquí ya no serializamos porque el repo actualizado lo hace. 
            # Si quieres que el servicio sea responsable de la serialización, 
            # deberías modificar el repositorio para que devuelva el modelo de SQLAlchemy.
            return usuario_actualizado
        return None

    def delete_usuario(self, id):
        resultado = self.usuario_repository.delete_usuario(id)
        return resultado