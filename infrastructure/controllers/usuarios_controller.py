# infrastructure/controllers/usuarios_controller.py (ACTUALIZADO)
from flask import Blueprint, request, jsonify
# from application.services.usuario_service import UsuarioService # Ya no la importamos para instanciar

usuarios_controller = Blueprint('usuarios_controller', __name__)

# Creamos un placeholder global para el servicio inyectado
_usuario_service = None

# Función para configurar el servicio inyectado. Llamada desde app.py.
def set_usuario_service(service):
    global _usuario_service
    _usuario_service = service
    print("UsuarioService inyectado en el controlador.")


@usuarios_controller.route('/usuarios', methods=['GET'])
def usuarios():
    # Usamos la instancia inyectada
    try:
        if _usuario_service is None:
             # Esto nunca debería pasar en producción si la configuración es correcta
            return jsonify({"error": "Servicio de usuario no configurado"}), 500
        
        resultado = _usuario_service.get_usuarios() 
        return jsonify(resultado)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500

@usuarios_controller.route('/usuarios', methods=['POST'])
def create_usuario():
    if _usuario_service is None:
        return jsonify({"error": "Servicio de usuario no configurado"}), 500
    
    print("USER|CONTROLLEER|CREATE|")
    # Usamos la instancia inyectada
    resultado = _usuario_service.create_usuario(request.json)
    if resultado:
        return jsonify(resultado), 201
    return jsonify({"error": "No se pudo crear el usuario"}), 400

@usuarios_controller.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    if _usuario_service is None:
        return jsonify({"error": "Servicio de usuario no configurado"}), 500
    
    print("USER|CONTROLLEER|UPDATE|", id)
    # Usamos la instancia inyectada
    resultado = _usuario_service.update_usuario(id, request.json)
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Usuario no encontrada"}), 404

@usuarios_controller.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    if _usuario_service is None:
        return jsonify({"error": "Servicio de usuario no configurado"}), 500
    
    print("USER|CONTROLLEER|DELETE|", id)
    # Usamos la instancia inyectada
    resultado = _usuario_service.delete_usuario(id)
    if resultado:
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    return jsonify({"error": "Usuario no encontrada"}), 404