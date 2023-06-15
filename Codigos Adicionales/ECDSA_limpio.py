
'''
Curvas elípticas y las funciones requeridas
para hacer las operaciones necesarias

Esta versión es la que se utilizara para ejecución de la solución
'''

import hashlib
import binascii
import secrets
import time
import csv
from Crypto.PublicKey import ECC
from cryptography import x509


#Calcular el Maximo comun divisor de dos numeros usan el algoritmo euclidiano extendido
def GCDExtended(a,b): #a,b son los numeros a encontrar
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1

    #Proceso del algoritmo para encontrar el GCD
    while b!= 0:
        q,a,b = a // b, b, a % b
        x0,x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0 #a es el GCD


#Calcular el inverso bajo un modulo p
def Inverso_calc(a, Fn): #a es el inverso a encontrar y Fn el mod p
    GCD ,x , y = GCDExtended(a,Fn)
    if GCD != 1:
        return False
    return x % Fn


#Calculo del inverso aditivo
def inverso_adi(x,p): #p es el modulo
    if x <= p-1:
        return p - x
    if x > p:
        return p - (x % p)
    
    
#Exponencial binaria, facilita las operaciones que se tienen que realizar dada la longitud de los digitos
'''
x es la base
n es el exponente, la función opera correctamente ÚNICAMENTE cuando n es primo
'''

def expo_binaria(x, n):
    res = 1
    q = n -2
    while q > 0:
        if q % 2 == 1:
            res = (res * x) % n
        x = (x * x) % n
        q = q // 2
    return res

#Calcular pendiente en la suma de las curvas
'''
p es el modulo en el que se esta trabajando
a es el coeficiente de la "x" lineal en la ecuación de la curva elíptica
xi, yi, son los puntos respectivos a sumar
'''
def pendiente(x1, y1, x2, y2, a, p): 
    if (x1 and y1) is None or (x2 and y2) is None: #Caso atipico que no se le de nada a la funcion
        return (x1, y1) or (x2, y2)
    if (x1 == x2 and y1 == y2): #Calculo de 2P, sumar el mismo punto
        return (((3 * x1 * x1) + a) * expo_binaria(2 * y1, p)) % p
    else: #Calculo de P + Q, puntos diferentes
        return ((y2 + inverso_adi(y1, p)) * expo_binaria(x2 + inverso_adi(x1, p), p)) % p
    

#Suma de puntos en una curva
'''
p es el modulo en el que se esta trabajando 
m es la funcion pendiente, se tiene que llamar a la función en los parametros
xi, yi son los puntos respectivos
'''
def Suma_Curva(x1,y1,x2,y2,m,p): 
    x3 = 0
    y3= 0

    x3 = (m * m + inverso_adi(x1,p) + inverso_adi(x2,p)) % p #Se calcula el punto x3, ambos casos de la suma son considerados
    y3 = (m * (x1 + inverso_adi(x3,p)) + inverso_adi(y1,p)) % p #Se calcular el punto y3, ambos casos de la curva son considerados
    return x3,y3


'''
Esta función es para el calculo de Q = dG de la referencia usada.
Para esto se tiene que trabajar en números binarios para que los calculos sean posibles de realizar
p es el modulo en el que se esta trabajando
a el coeficiente lineal de la curva eliptica
n es el escalar a multiplicar
Implementación del algoritmo double and add, en el reporte se puede encontrar la referencia de su funcionamiento
'''
def mult_binaria(x, y, a, p, n):
    n = bin(n)[3:] #bin() da la representación binaria de un integer
    x2 = x
    y2 = y
    for i in n:
        if i == '1':
            m = pendiente(x2, y2, x2, y2, a, p)
            x2, y2 = Suma_Curva(x2, y2, x2, y2, m, p)
            m = pendiente(x2, y2, x, y, a, p)
            x2, y2 = Suma_Curva(x, y, x2, y2, m, p)

        if i == '0':
            m = pendiente(x2, y2, x2, y2, a, p)
            x2, y2 = Suma_Curva(x2, y2, x2, y2, m, p)

    return x2, y2


def obtener_llave_privada(): #da la clave privada, que es el escalar para la mult_binaria, utilizada para numeros pseudo-aleatorios
    #El valor escalar es el definido por la curva NIST P - 256
    n = int(0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551)
    return int(secrets.randbelow(n-1) + 1)


#Obtencion de llave privada del certificado generado
def llave_privada_cert():

    f = open('C:\\Users\\moeug\\OneDrive\\Documentos\\algebras modernas\\client.key')

    key = ECC.import_key(f.read())

    return int(key.d)


#Obtención de llave privada generada por certificado

def llave_publica_cert():

    certificate_file = open("client.crt","rb")
    cert_to_check = x509.load_pem_x509_certificate(certificate_file.read())
    gx = cert_to_check.public_key().public_numbers().x
    gy = cert_to_check.public_key().public_numbers().y

    return int(gx),int(gy)



'''
Función para obtener los parametros de la curva a utilizar
La descripción de los valores se encuentra en el reporte realizado
'''
def Parametros_curva():
    # Valores definidos por la curva NIST P-256
    p = int(0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff)
    a = int(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc)
    b = int(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
    gx = int(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296)
    gy = int(0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
    n = int(0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551)

    return p,a,b,gx,gy,n   


#Metodo de firma ECDSA tomado de la referencia del reporte
def firmar_mensaje(mensaje,llave_priv):

    #Se llaman a los parametros de la curva NIST P-256
    p,a,b,gx,gy,n = Parametros_curva()

    #1.-Generar numero aleatorio "k" 1 < k < n-1
    k = obtener_llave_privada()

    #2.- Calcular kG = (x1,y1), clave publica
    x1, y1 = mult_binaria(gx, gy, a, p, k)
    x1 = int(x1)

    #3.-Calcular r = x1 mod n, si r = 0 regresar al paso 1
    r = x1 % n
    if r == 0:
        return firmar_mensaje(mensaje, llave_priv)

    #4.-Calcular inverso de k mod n
    inversoK = Inverso_calc(k, n)

    #5.-Calcular sha-1(mensaje) y convertir el string en un entero "e"
    hash_object = hashlib.sha256()
    hash_object.update(mensaje.encode())
    hexa = binascii.hexlify(hash_object.digest())
    e = int(hexa,16)

    #6.- Calcular m = kinverso(e +dr) mod n, si m = 0 regresar al paso 1

    m = (inversoK * (e + llave_priv * r)) % n
    if m == 0:
        return firmar_mensaje(mensaje, llave_priv)

    #7.- A's signature of the message m is (r,s)  
    return (r,m)


def verificar_firma(r, s, m, n, G, Q, a):

    #1.-Verificar que r y s son enteros en el intervalos en [1,n-1]
    if not(1 <= r <= n-1 and 1 <= s <= n-1):
        return 'Paso 1 del proceso de verificación no cumplido'
    
    #2.-Calcular SHA(mensaje) y convertir a un entero "e"
    hash_object = hashlib.sha256 ()
    hash_object.update(m.encode())
    hexa = binascii.hexlify(hash_object.digest())
    e = int( hexa ,16)

    #3.- Calcular w = s^-1 mod n
    w = Inverso_calc(s,n)

    #4.- Calcular u1 = ew mod n y w2 = rw mod n

    u1 = (e * w) % n
    u2 = (r * w) % n

    #5.- Calcular X = u1G + u2Q

    x1, y1 = mult_binaria(G[0], G[1], a, p, u1)
    x2, y2 = mult_binaria(Q[0], Q[1], a, p, u2)
    pendi = pendiente(x1,y1,x2,y2, a, p)
    x3, y3 = Suma_Curva(x1,y1,x2,y2, pendi, p)

    '''
    6.- Si X = 0 entonces rechazar
    De lo contrario, convertir  x coordenada x1 de X a entero y calcular v = x1 mod n
    '''

    if (x3, y3) == (0,0):
        return 'Firma rechazada'
    
    #7.- Aceptar la firma unicamente si v = r
    v = x3 % n

    #if v == r:
    #    return 'Firma verificada'
    
    return print(f'Verificación de la firma: {v == r}')

#Ejemplo de vectores de prueba

p,a,b,gx,gy,n = Parametros_curva()
x = llave_privada_cert()
Gx,Gy = llave_publica_cert()
Ux , Uy = mult_binaria (gx , gy ,a ,p , x)


'''
Prueba  de lectura de tramas en intervalos de las tramas
'''


def Leerconsumo():
    file = open("TramasConsumo.csv", 'r')

    text = file.readline()
    start_time = time.time()
    while text !="":
        #start_time = time.time()
        text = file.readline()
        ' '.join(text)
        print(text)
        time.sleep(1)
        r,s = firmar_mensaje(text,x)
        verificar_firma(r,s,text,n,(gx,gy),(Ux,Uy),a)
        #print("--- %s seconds ---" % (time.time() - start_time))
        print('\n')
    print("--- %s seconds ---" % (time.time() - start_time))

def LeerProduccion():
    file = open("TramasProduccion.csv", 'r')

    #text = file.readline()
    start_time = time.time()
    while text !="":
        #start_time = time.time()
        text = file.readline()
        ' '.join(text)
        print(text)
        time.sleep(1)
        r,s = firmar_mensaje(text,x)
        verificar_firma(r,s,text,n,(gx,gy),(Ux,Uy),a)
        #print("--- %s seconds ---" % (time.time() - start_time))
        print('\n')
    print("--- %s seconds ---" % (time.time() - start_time))

#print(Gx == Ux)
#print(Gy == Uy)

#Leerconsumo()
#LeerProduccion()