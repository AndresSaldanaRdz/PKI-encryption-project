from pkiwebapp import db
from datetime import date
#from flask_login import UserMixin

class Crypto(db.Model): 

    __tablename__ = 'cryptos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=date.today)
    intervalo = db.Column(db.Integer)
    medida = db.Column(db.Float)
    identificador = db.Column(db.String(64))

    def __init__(self, fecha, intervalo, medida, identificador):
        self.fecha = fecha
        self.intervalo = intervalo
        self.medida = medida
        self.identificador = identificador

    def __repr__(self):
        return f"ID: {self.id} - Fecha: {self.fecha} - Intervalo: {self.intervalo} - Medida: {self.medida} - Identificador: {self.identificador}"

class Tiempo(db.Model): 

    __tablename__ = 'tiempos'

    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Integer)

    def __init__(self, dato):
        self.dato = dato

    def __repr__(self):
        return f"ID: {self.id} - Dato: {self.dato}"