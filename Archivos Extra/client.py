# Esta libreria la utilizamos para encriptar la información de manera asimetrica
import rsa
# Esta libreria la utilizamos para crear la conexión entre el servidor y el raspberry pi
import socket
# Esta libreria la utilizamos para leer archivos csv
import csv
# Esta libreria la utilizamos para crear el delay entre el envío de los datos
import time

# En esta linea abrimos el archivo public.pem para poder cifrar información antes de enviarla
with open("public.pem","rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# En esta parte hacemos la conexión al servidor en el puerto y dirección IP.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('3.142.114.187',4545)) 

# En esta parte pongo los nombres de los archivos que se estan utilizando.

filename = 'ProdCons.csv'
tiempo = 'Tiempo.csv'

# En esta parte abrimos los archivos csv iteramos en ellos y los encriptamos y enviamos al centro de control en el servidor
# tambien estamos escuchando por el tiempo que necesitamos que usar como delay en lo que mandamos la siguiente linea.

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader)
    for row in datareader:
        with open(tiempo, 'r') as tiempofile:

            rowArray  = row
            rowString = ",".join(row)


            encrypted_message = rsa.encrypt(rowString.encode(),public_key)
            s.send(encrypted_message)
            print(rowString)



            nuevoTiempo = s.recv(1024)
            nuevoTiempo = nuevoTiempo.decode()
            nuevoTiempo = int(nuevoTiempo)
            print(nuevoTiempo)
            time.sleep(nuevoTiempo)
            
