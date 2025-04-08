# backend/blueprints/auth_blueprint.py

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

auth_blueprint = Blueprint('auth_blueprint', __name__)

# Usuario simulado para demo
USERS = {
    "admin": "1234"
}

SECRET_KEY = os.getenv("SECRET_KEY", "secreto-demo")

@auth_blueprint.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if USERS.get(username) == password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'token': token})

    return jsonify({'error': 'Credenciales inválidas'}), 401