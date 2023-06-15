import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import timedelta
from OpenSSL import SSL

app = Flask(__name__)

load_dotenv()  # cargamos el archivo oculto .env
app.config['SECRET_KEY'] = os.environ.get('LLAVE_SECRETA')   # configuramos la llave secreta para la aplicacion

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')   # establecemos el url de conexion hacia la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # creamos una instancia de la base de datos con sqlalchemy

from pkiwebapp.core.views import core

app.register_blueprint(core)  # registramos los archivos .py que usaremos despues
