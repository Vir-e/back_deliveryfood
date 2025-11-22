from config.database import get_db, Session
from models.carta_model import CartaModel
from infrastructure.datamappers.schemas.carta_schema import CartaSchema

class CartaRepository:
    def __init__(self):
        # No mantener la sesión como atributo de instancia
        pass

    def _get_session(self):
        """Obtener una nueva sesión"""
        return next(get_db())

    def get_carta(self):
        db = self._get_session()
        try:
            cartas = db.query(CartaModel).all()
            # Expulsar los objetos de la sesión para que puedan ser serializados
            for carta in cartas:
                db.expunge(carta)
            return cartas
        except Exception as e:
            print(e)
            db.rollback()
            return []
        finally:
            db.close()

    def create_carta(self, carta_model):
        db = self._get_session()
        try:
            db.add(carta_model)
            db.commit()
            db.refresh(carta_model)
            # Expulsar el objeto de la sesión
            db.expunge(carta_model)
            return carta_model
        except Exception as e:
            print(e)
            db.rollback()
            return None
        finally:
            db.close()

    def update_carta(self, carta_model):
        db = self._get_session()
        try:
            # Primero obtener la carta existente
            carta_existente = db.query(CartaModel).filter(CartaModel.id == carta_model.id).first()
            if not carta_existente:
                return None
            
            # Actualizar los campos
            carta_existente.nombre = carta_model.nombre
            carta_existente.precio = carta_model.precio
            
            db.commit()
            # Expulsar el objeto de la sesión antes de cerrarla
            db.refresh(carta_existente)
            schema = CartaSchema()
            resultado = schema.dump(carta_existente)
            return resultado
        except Exception as e:
            print(e)
            db.rollback()
            return None
        finally:
            db.close()

    def delete_carta(self, id):
        db = self._get_session()
        try:
            carta_model = db.query(CartaModel).filter(CartaModel.id == id).first()
            if not carta_model:
                return False
            db.delete(carta_model)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()