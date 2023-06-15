from pkiwebapp import db
from datetime import date

# aqui delcaramos las tablas de la base de datos, es decir cuando utlizemos el comando db.create(all)
class Crypto(db.Model): # esta tabla se llama Crypto

    __tablename__ = 'cryptos'

    id = db.Column(db.Integer, primary_key=True) # la columana identificadora
    fecha = db.Column(db.Date, default=date.today()) # la fecha usando formato date time
    intervalo = db.Column(db.Integer) # columna que almacena numeros
    medida = db.Column(db.Float) # columna que almacena strings
    identificador = db.Column(db.String(64))

    def __init__(self, fecha, intervalo, medida, identificador): # declaramos el constructor
        self.fecha = fecha
        self.intervalo = intervalo
        self.medida = medida
        self.identificador = identificador

    def __repr__(self): # la representacion sting para cuando queremos imprimir un renglon
        return f"ID: {self.id} - Fecha: {self.fecha} - Intervalo: {self.intervalo} - Medida: {self.medida} - Identificador: {self.identificador}"

class Tiempo(db.Model):

    __tablename__ = 'tiempos'

    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Integer)

    def __init__(self, dato):
        self.dato = dato

    def __repr__(self):
        return f"ID: {self.id} - Dato: {self.dato}"