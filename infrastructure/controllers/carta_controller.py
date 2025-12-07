# infrastructure/controllers/carta_controller.py (ACTUALIZADO)
from flask import Blueprint, request, jsonify
# from application.services.carta_service import CartaService # Eliminado

carta_controller = Blueprint('carta_controller', __name__)

# Placeholder global para el servicio inyectado
_carta_service = None

# Función para configurar el servicio inyectado (llamada desde app.py)
def set_carta_service(service):
    global _carta_service
    _carta_service = service


@carta_controller.route('/carta', methods=['GET'])
def carta():
    # Usamos la instancia inyectada
    if _carta_service is None:
        return jsonify({"error": "Servicio de carta no configurado"}), 500
    
    resultado = _carta_service.get_carta()
    return jsonify(resultado)

@carta_controller.route('/carta', methods=['POST'])
def create_carta():
    if _carta_service is None:
        return jsonify({"error": "Servicio de carta no configurado"}), 500
        
    resultado = _carta_service.create_carta(request.json)
    if resultado:
        return jsonify(resultado), 201
    return jsonify({"error": "No se pudo crear la carta"}), 400

@carta_controller.route('/carta/<int:id>', methods=['PUT'])
def update_carta(id):
    if _carta_service is None:
        return jsonify({"error": "Servicio de carta no configurado"}), 500
        
    resultado = _carta_service.update_carta(id, request.json)
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Carta no encontrada"}), 404

@carta_controller.route('/carta/<int:id>', methods=['DELETE'])
def delete_carta(id):
    if _carta_service is None:
        return jsonify({"error": "Servicio de carta no configurado"}), 500
        
    resultado = _carta_service.delete_carta(id)
    if resultado:
        return jsonify({"message": "Carta eliminada correctamente"}), 200
    return jsonify({"error": "Carta no encontrada"}), 404