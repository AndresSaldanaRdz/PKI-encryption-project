import rsa
import socket
import csv
import time


with open("public.pem","rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

#message = "Yo"
#encrypted_message = rsa.encrypt(message.encode(),public_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('3.142.114.187',4545)) 

filename = 'ProdCons.csv'
tiempo = 'Tiempo.csv'

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
            
