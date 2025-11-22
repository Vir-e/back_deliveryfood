from flask import Blueprint, request, jsonify
from application.services.producto_service import ProductoService

productos_controller = Blueprint('productos_controller', __name__)

@productos_controller.route('/productos', methods=['GET'])
def productos():
    resultado = ProductoService().get_productos()
    return jsonify(resultado)

@productos_controller.route('/productos', methods=['POST'])
def create_producto():
    resultado = ProductoService().create_producto(request.json)
    if resultado:
        return jsonify(resultado), 201
    return jsonify({"error": "No se pudo crear el producto"}), 400

@productos_controller.route('/producto/<int:id>', methods=['PUT'])
def update_producto(id):
    resultado = ProductoService().update_producto(id, request.json)
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Producto no encontrada"}), 404

@productos_controller.route('/producto/<int:id>', methods=['DELETE'])
def delete_producto(id):
    resultado = ProductoService().delete_producto(id)
    if resultado:
        return jsonify({"message": "Producto eliminada correctamente"}), 200
    return jsonify({"error": "Producto no encontrada"}), 404