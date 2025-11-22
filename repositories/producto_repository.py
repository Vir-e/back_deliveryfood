from config.database import get_db, Session
from models.producto_model import ProductoModel
from infrastructure.datamappers.schemas.producto_schema import ProductoSchema

class ProductoRepository:
    def __init__(self):
        # No mantener la sesión como atributo de instancia
        pass

    def _get_session(self):
        """Obtener una nueva sesión"""
        return next(get_db())

    def get_productos(self):
        db = self._get_session()
        try:
            productos = db.query(ProductoModel).all()
            # Expulsar los objetos de la sesión para que puedan ser serializados
            for producto in productos:
                db.expunge(producto)
            return productos
        except Exception as e:
            print(e)
            db.rollback()
            return []
        finally:
            db.close()

    def create_producto(self, producto_model):
        db = self._get_session()
        try:
            db.add(producto_model)
            db.commit()
            db.refresh(producto_model)
            # Expulsar el objeto de la sesión
            db.expunge(producto_model)
            return producto_model
        except Exception as e:
            print(e)
            db.rollback()
            return None
        finally:
            db.close()

    def update_producto(self, producto_model, id=None):
        db = self._get_session()
        try:
            # Usar el id del parámetro o del modelo
            producto_id = id if id is not None else producto_model.id
            if producto_id is None:
                return None
                
            # Primero obtener el producto existente
            producto_existente = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
            if not producto_existente:
                return None
            
            # Actualizar los campos
            producto_existente.nombre = producto_model.nombre
            producto_existente.precio_kg = producto_model.precio_kg
            producto_existente.stock = producto_model.stock
            
            db.commit()
            # Expulsar el objeto de la sesión antes de cerrarla
            db.refresh(producto_existente)
            schema = ProductoSchema()
            resultado = schema.dump(producto_existente)
            return resultado
        except Exception as e:
            print(e)
            db.rollback()
            return None
        finally:
            db.close()

    def delete_producto(self, id):
        db = self._get_session()
        try:
            producto_model = db.query(ProductoModel).filter(ProductoModel.id == id).first()
            if not producto_model:
                return False
            db.delete(producto_model)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()

