from repositories.producto_repository import ProductoRepository
from infrastructure.datamappers.schemas.producto_schema import ProductoSchema
from models.producto_model import ProductoModel


class ProductoService:
    def __init__(self):
        self.producto_repository = ProductoRepository()
        self.schema = ProductoSchema()
        self.schema_list = ProductoSchema(many=True)
        
    def get_productos(self):
        productos_model = self.producto_repository.get_productos()
        # Serializar inmediatamente
        return self.schema_list.dump(productos_model)

    def create_producto(self, producto_data):
        producto_model = ProductoModel(
            nombre=producto_data['nombre'],
            precio_kg=producto_data['precio'],
            stock=producto_data['stock']
        )
        producto_creado = self.producto_repository.create_producto(producto_model)
        if producto_creado:
            # Serializar antes de devolver
            return self.schema.dump(producto_creado)
        return None

    def update_producto(self, id, producto_data):
        producto_model = ProductoModel(
            nombre=producto_data['nombre'],
            precio_kg=producto_data['precio'],
            stock=producto_data['stock']
        )
        producto_actualizado = self.producto_repository.update_producto(producto_model, id)
        if producto_actualizado:
            return producto_actualizado

    def delete_producto(self, id):
        resultado = self.producto_repository.delete_producto(id)
        return resultado