# infrastructure/repositories/carta_repository.py (ACTUALIZADO)
from models.carta_model import CartaModel
from infrastructure.datamappers.schemas.carta_schema import CartaSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class CartaRepository:
    """
    La sesión de DB (db) es inyectada en el constructor.
    """
    def __init__(self, db: Session): 
        # ⚠️ INYECCIÓN DE DEPENDENCIA: Recibe la sesión de DB
        self.db = db

    # El método _get_session() ha sido ELIMINADO

    def get_carta(self):
        try:
            cartas = self.db.query(CartaModel).all()
            # Expulsar los objetos de la sesión
            for carta in cartas:
                self.db.expunge(carta)
            return cartas
        except SQLAlchemyError as e:
            print(f"Error al obtener cartas: {e}")
            self.db.rollback()
            return []
        # ELIMINADO: finally: db.close()

    def create_carta(self, carta_model):
        try:
            self.db.add(carta_model)
            self.db.commit()
            self.db.refresh(carta_model)
            # Expulsar el objeto de la sesión
            self.db.expunge(carta_model)
            return carta_model
        except SQLAlchemyError as e:
            print(f"Error al crear carta: {e}")
            self.db.rollback()
            return None
        # ELIMINADO: finally: db.close()

    def update_carta(self, carta_model):
        try:
            carta_existente = self.db.query(CartaModel).filter(CartaModel.id == carta_model.id).first()
            if not carta_existente:
                return None
            
            carta_existente.nombre = carta_model.nombre
            carta_existente.precio = carta_model.precio
            
            self.db.commit()
            self.db.refresh(carta_existente)
            
            # Serializar el resultado aquí para devolver un DTO/dict
            schema = CartaSchema() 
            resultado = schema.dump(carta_existente)
            self.db.expunge(carta_existente)
            return resultado
        except SQLAlchemyError as e:
            print(f"Error al actualizar carta: {e}")
            self.db.rollback()
            return None
        # ELIMINADO: finally: db.close()

    def delete_carta(self, id):
        try:
            carta_model = self.db.query(CartaModel).filter(CartaModel.id == id).first()
            if not carta_model:
                return False
            self.db.delete(carta_model)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error al eliminar carta: {e}")
            self.db.rollback()
            return False
        # ELIMINADO: finally: db.close()