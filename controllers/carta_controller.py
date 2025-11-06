from flask import Blueprint, request, jsonify
from services.carta_service import CartaService

carta_controller = Blueprint('carta_controller', __name__)

@carta_controller.route('/carta', methods=['GET'])
def carta():
    resultado = CartaService().get_carta()
    return jsonify(resultado)

@carta_controller.route('/carta', methods=['POST'])
def create_carta():
    resultado = CartaService().create_carta(request.json)
    if resultado:
        return jsonify(resultado), 201
    return jsonify({"error": "No se pudo crear la carta"}), 400

@carta_controller.route('/carta/<int:id>', methods=['PUT'])
def update_carta(id):
    resultado = CartaService().update_carta(id, request.json)
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Carta no encontrada"}), 404

@carta_controller.route('/carta/<int:id>', methods=['DELETE'])
def delete_carta(id):
    resultado = CartaService().delete_carta(id)
    if resultado:
        return jsonify({"message": "Carta eliminada correctamente"}), 200
    return jsonify({"error": "Carta no encontrada"}), 404