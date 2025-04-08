# backend/utils.py

import jwt
from flask import request, jsonify
import os
from functools import wraps  


SECRET_KEY = os.getenv("SECRET_KEY", "secreto-demo")

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token es necesario!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalido!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorator
