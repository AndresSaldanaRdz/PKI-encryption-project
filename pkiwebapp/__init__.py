import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from datetime import timedelta 

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('LLAVE_SECRETA') 


app.config['SQLALCHEMY_DATABASE_URI'] = " "
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# login_manager = LoginManager() 
# login_manager.init_app(app) 
# login_manager.login_view = 'core.homeview' 

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

from pkiwebapp.core.views import core

app.register_blueprint(core)

# poner l de loged in manager para que sea seguro
# crear la base de datos
