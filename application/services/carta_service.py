# application/services/carta_service.py (ACTUALIZADO - Asumiendo la lógica de servicio)
# Importamos las dependencias internas
from models.carta_model import CartaModel
from infrastructure.datamappers.schemas.carta_schema import CartaSchema
# No necesitamos importar CartaRepository si se inyecta

class CartaService:
    # ⚠️ INYECCIÓN DE DEPENDENCIA: Recibe el repositorio y los esquemas
    def __init__(self, carta_repository, schema: CartaSchema, schema_list: CartaSchema):
        self.carta_repository = carta_repository
        self.schema = schema
        self.schema_list = schema_list

    def get_carta(self):
        try:
            cartas_model = self.carta_repository.get_carta()
            # Serializar la lista antes de devolver
            return self.schema_list.dump(cartas_model)
        except Exception as e:
            print(f"Error en get_carta del servicio: {e}")
            return []

    def create_carta(self, carta_data):
        try:
            carta_model = CartaModel(
                nombre=carta_data['nombre'],
                precio=carta_data['precio']
            )
            carta_creada = self.carta_repository.create_carta(carta_model)
            if carta_creada:
                # Serializar antes de devolver
                return self.schema.dump(carta_creada)
            return None
        except Exception as e:
             print(f"Error en create_carta del servicio: {e}")
             return None

    def update_carta(self, id, carta_data):
        try:
            carta_model = CartaModel(
                id=id,
                nombre=carta_data.get('nombre'),
                precio=carta_data.get('precio')
            )
            # El repositorio actualizado devuelve el resultado serializado (dict)
            carta_actualizada = self.carta_repository.update_carta(carta_model)
            return carta_actualizada
        except Exception as e:
             print(f"Error en update_carta del servicio: {e}")
             return None


    def delete_carta(self, id):
        resultado = self.carta_repository.delete_carta(id)
        return resultado