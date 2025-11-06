from repository.carta_repository import CartaRepository
from datamappers.carta_datamapper import CartaSchema
from models.domain.carta import Carta


class CartaService:
    def __init__(self):
        self.carta_repository = CartaRepository()
        self.schema = CartaSchema()
        self.schema_list = CartaSchema(many=True)
        
    def get_carta(self):
        cartas_model = self.carta_repository.get_carta()
        # Serializar inmediatamente
        return self.schema_list.dump(cartas_model)

    def create_carta(self, carta_data):
        carta_model = Carta(
            nombre=carta_data['nombre'],
            precio=carta_data['precio'],
            sin_gluten=carta_data['sin_gluten'],
            sin_huevo=carta_data['sin_huevo'],
            vegano=carta_data['vegano']
        )
        carta_creada = self.carta_repository.create_carta(carta_model)
        if carta_creada:
            # Serializar antes de devolver
            return self.schema.dump(carta_creada)
        return None

    def update_carta(self, id, carta_data):
        carta_model = Carta(
            id=id,
            nombre=carta_data['nombre'],
            precio=carta_data['precio'],
            sin_gluten=carta_data['sin_gluten'],
            sin_huevo=carta_data['sin_huevo'],
            vegano=carta_data['vegano']
        )
        carta_actualizada = self.carta_repository.update_carta(carta_model)
        if carta_actualizada:
            return carta_actualizada

    def delete_carta(self, id):
        resultado = self.carta_repository.delete_carta(id)
        return resultado