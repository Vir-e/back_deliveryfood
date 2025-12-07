# app.py (ACTUALIZADO - Añadiendo el setup de DI)
from flask import Flask, g
from infrastructure.controllers.carta_controller import carta_controller, set_carta_service
from infrastructure.controllers.productos_controller import productos_controller
from infrastructure.controllers.usuarios_controller import usuarios_controller, set_usuario_service # Importamos la función de inyección

# Importar las clases de dependencia necesarias
from application.services.usuario_service import UsuarioService
from repositories.usuario_repository import UsuarioRepository
from infrastructure.datamappers.schemas.usuario_schema import UsuarioSchema
from config.database import get_db # Necesitamos la función generadora de sesiones

from application.services.carta_service import CartaService
from repositories.carta_repository import CartaRepository
from infrastructure.datamappers.schemas.carta_schema import CartaSchema

from flask_cors import CORS
import settings


# --- Creación de la Aplicación (Application Factory Pattern) ---

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 1. Configuración del Contexto de la Base de Datos (DB Session)
    # Esto asegura que get_db() se ejecute al inicio y cierre al final de CADA solicitud.
    
    # Creamos un decorador que inyectará el objeto de sesión (db) en el contexto de la solicitud
    @app.before_request
    def before_request():
        # Inicializa el generador de DB y guarda la sesión en el objeto 'g' (global-context) de Flask
        g.db_gen = get_db()
        g.db = next(g.db_gen) 

    @app.teardown_request
    def teardown_request(exception=None):
        # Cierra la sesión de DB al final de la solicitud
        db_gen = getattr(g, 'db_gen', None)
        if db_gen is not None:
            try:
                # El generador de get_db() contiene el bloque finally, que ejecuta db.close()
                next(db_gen) 
            except StopIteration:
                pass # Es normal que el generador lance StopIteration al finalizar

    # 2. Configuración de la Inyección de Dependencias (DI Setup)
    
    # **Factoría/Clausura para el UsuarioService**
    # Esta función crea y devuelve el UsuarioService (y sus dependencias)
    # en el contexto de la solicitud, asegurando que usa la sesión g.db
    def get_injected_usuario_service():
        # Recupera la sesión inyectada en el contexto de la solicitud
        db_session = getattr(g, 'db', None) 
        if db_session is None:
            raise RuntimeError("La sesión de la base de datos (g.db) no está disponible.")

        # Inyección: Repositorio depende de la Sesión de DB
        usuario_repository = UsuarioRepository(db=db_session)
        
        # Inyección: Servicio depende del Repositorio y los Schemas
        usuario_service = UsuarioService(
            usuario_repository=usuario_repository,
            schema=UsuarioSchema(),
            schema_list=UsuarioSchema(many=True)
        )
        return usuario_service


        # FUNCIÓN INYECTABLE PARA CARTA
    def get_injected_carta_service():
        db_session = getattr(g, 'db', None)
        if db_session is None:
             raise RuntimeError("La sesión de la base de datos (g.db) no está disponible.")
             
        # Inyección: Repositorio depende de la Sesión de DB
        carta_repository = CartaRepository(db=db_session)
        
        # Inyección: Servicio depende del Repositorio y los Schemas
        carta_service = CartaService(
            carta_repository=carta_repository,
            schema=CartaSchema(),
            schema_list=CartaSchema(many=True)
        )
        return carta_service

    # 3. Inyección del Servicio en el Controlador (Inyección a nivel de aplicación)
    # Como Flask no soporta DI nativa en las rutas, inyectamos un "Singleton-per-request-aware" 
    # a través de un proxy que siempre llama a la función anterior (get_injected_usuario_service)
    # cada vez que se usa el servicio dentro de una vista.
    
    # ⚠️ Nota: Este es un proxy muy simplificado para tu ejemplo. 
    # En un caso real, usarías un Singleton o un DI Container.
    class UsuarioServiceProxy:
        def __getattr__(self, name):
            # Cada vez que se accede a un método (get_usuarios, create_usuario, etc.), 
            # se crea un nuevo UsuarioService que usa la sesión de la solicitud (g.db).
            service_instance = get_injected_usuario_service()
            return getattr(service_instance, name)

    # PROXY PARA CARTA (NUEVO)
    class CartaServiceProxy:
        def __getattr__(self, name):
            service_instance = get_injected_carta_service()
            return getattr(service_instance, name)


    # Inyectamos el Proxy en el controlador al inicio
    set_usuario_service(UsuarioServiceProxy()) 
    set_carta_service(CartaServiceProxy())


    @app.route('/')
    def index():
        return "Hello, World!"

    # 4. Registro de Blueprints
    app.register_blueprint(carta_controller)
    app.register_blueprint(productos_controller)
    app.register_blueprint(usuarios_controller)
    
    return app

# Ejecución (Si app.py es el punto de inicio)
app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
