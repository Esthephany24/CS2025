#app.py

from flask import Flask,  request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from backend.blueprints.autores_blueprint import autor_blueprint
from backend.blueprints.libros_blueprint import libro_blueprint
from backend.blueprints.auth_blueprint import auth_blueprint

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

JWTManager(app)

app.register_blueprint(autor_blueprint, url_prefix='/home')
app.register_blueprint(libro_blueprint, url_prefix='/home')
app.register_blueprint(auth_blueprint, url_prefix='/auth')

cors = CORS(app)

if __name__ == "__main__":
    app.run(debug=True)