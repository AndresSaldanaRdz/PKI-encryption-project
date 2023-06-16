import rsa
import socket
import psycopg2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",4545))
s.listen()

conn = psycopg2.connect(
        dbname = "Cripto",
        host = "database-1.cxo39yraj8pu.us-east-2.rds.amazonaws.com",
        port = 5432,
        user = "Gil",
        password = "Eugenius"
)

with open("private.pem","rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

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

cur.close()
conn.close()
