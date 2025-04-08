# backend/blueprints/autores_blueprint.py

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from backend.models.mysql_autores_model import AutorModel
from backend.utils import token_required

model = AutorModel()
autor_blueprint = Blueprint('autor_blueprint', __name__)

@autor_blueprint.route('/crearautor', methods=['POST'])
@cross_origin()
@token_required # para proteger el endpoint
def create_autor(current_user):
    try:
        data = model.create_autor(request.json['nombre'], request.json.get('nacionalidad'))
        return jsonify(data),201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@autor_blueprint.route('/actualizarautor', methods=['PUT'])
@cross_origin()
@token_required # para proteger el endpoint
def update_autor(current_user):
    try:
        data = model.update_autor(
            request.json['id'],
            request.json['nombre'],
            request.json.get('nacionalidad')
        )
        return jsonify(data),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@autor_blueprint.route('/eliminarautor', methods=['DELETE'])
@cross_origin()
@token_required # para proteger el endpoint
def delete_autor(current_user):
    try:
        return jsonify(model.delete_autor(int(request.json['id']))),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@autor_blueprint.route('/obtenerautor/<int:id>', methods=['GET'])
@cross_origin()
def get_autor(id):
    try: 
        return jsonify(model.get_autor(id)),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@autor_blueprint.route('/obtenerautores', methods=['GET'])
@cross_origin()
def get_autores():
    try:
        return jsonify(model.get_autores()),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#PARA PROBAR
@autor_blueprint.route('/test', methods=['GET'])
def test():
    return "Blueprint funciona"
