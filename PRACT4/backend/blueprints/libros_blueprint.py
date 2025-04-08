# backend/blueprints/libros_blueprint.py

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from backend.models.mysql_libros_model import LibroModel
from backend.utils import token_required

model = LibroModel()
libro_blueprint = Blueprint('libro_blueprint', __name__)

@libro_blueprint.route('/crearlibro', methods=['POST'])
@cross_origin()
def create_libro():
    data = model.create_libro(
        request.json['titulo'],
        request.json['año_publicacion'],
        request.json['id_autor']
    )
    return jsonify(data)

@libro_blueprint.route('/actualizarlibro', methods=['PUT'])
@cross_origin()
def update_libro():
    libro_id = request.json['id']
    titulo = request.json['titulo']
    año_publicacion = request.json['año_publicacion']
    id_autor = request.json.get('id_autor')
    if id_autor is None:
        id_autor = None
    data = model.update_libro(libro_id, titulo, año_publicacion, id_autor)
    return jsonify(data)

@libro_blueprint.route('/eliminarlibro', methods=['DELETE'])
@cross_origin()
def delete_libro():
    libro_id = int(request.json['id'])
    result = model.delete_libro(libro_id)
    return jsonify(result)

@libro_blueprint.route('/obtenerlibro/<int:id>', methods=['GET'])
@cross_origin()
def get_libro(id):
    return jsonify(model.get_libro(id))

@libro_blueprint.route('/obtenerlibros', methods=['GET'])
@cross_origin()
def get_libros():
    return jsonify(model.get_libros())

#nuevos endpoints

@libro_blueprint.route('/libros/autor/<int:id_autor>', methods=['GET'])
@token_required
@cross_origin()
def libros_por_autor(current_user, id_autor):
    libros = model.get_libros_por_autor(id_autor)
    return jsonify(libros),200

@libro_blueprint.route('/autores/libro/<int:id_libro>', methods=['GET'])
@token_required
@cross_origin()
def autores_por_libro(current_user, id_libro):
    autores = model.get_autores_por_libro(id_libro)
    return jsonify(autores),200


@libro_blueprint.route('/libros/<int:id_libro>/generos', methods=['POST'])
@token_required
@cross_origin()
def asignar_generos(current_user, id_libro):
    data = request.get_json()
    generos = data.get('generos')
    return model.asignar_generos(id_libro, generos)

@libro_blueprint.route('/libros/<int:id_libro>', methods=['DELETE'])
@token_required
@cross_origin()
def eliminar_libro(current_user, id_libro):
    return model.eliminar_libro(id_libro)
