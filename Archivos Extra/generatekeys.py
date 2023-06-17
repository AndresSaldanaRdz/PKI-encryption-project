# Esta libreria la utilizamos para encriptar la información de manera asimetrica

import rsa

# Generamos llaves nuevas para utilizar (par)

public_key,private_key = rsa.newkeys(1024)

# Las guardamos como public y private en formato .pem

with open("public.pem","wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

with open("private.pem","wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
