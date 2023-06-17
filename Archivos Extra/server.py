# Esta libreria la utilizamos para encriptar la información de manera asimetrica
import rsa
# Esta libreria la utilizamos para crear la conexión entre el servidor y el raspberry pi
import socket
# Esta libreria la utilizamos para hacer queries a la base de datos en RDS
import psycopg2

# Aquí elegimos un puerto y abrimos la conexión para escuchar inbound connections.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",4545))
s.listen()

# Aquí almacenamos los detalles de la conexión a la base de datos

conn = psycopg2.connect(
        dbname = "Cripto",
        host = "database-1.cxo39yraj8pu.us-east-2.rds.amazonaws.com",
        port = 5432,
        user = "Gil",
        password = "Eugenius"
)

# Aquí abrimos la el archivo private.pem para poder utilizarlo para decifrar información

with open("private.pem","rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# Aqui estamos aceptando conexiones recibiendo información y enviandola a la base de datos de lo que nos llega del auditor

client,address = s.accept()
print("Connected")
while True:
    cur = conn.cursor()
    tiempo = '1'
    message = client.recv(2048)
    decrypted_message = rsa.decrypt(message,private_key)
    decrypted_message = decrypted_message.decode()
    randomThing = decrypted_message.split(',')
    sql2 = cur.mogrify("""INSERT INTO cryptos(id, fecha, intervalo,medida,identificador)
    SELECT %s, %s, %s,%s,%s
    WHERE
    NOT EXISTS (
    SELECT id FROM cryptos WHERE id = %s
    );""",(randomThing[0],randomThing[2],randomThing[3],randomThing[4],randomThing[1],randomThing[0]))
    cur.execute(sql2)
    conn.commit()

    tiempo = tiempo.encode()
    client.send(tiempo)

# Cerramos el cursor y la conexión.

cur.close()
conn.close()
