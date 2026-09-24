#Libreria para anotar los endpoints
from fastapi import APIRouter
router = APIRouter()

import bcrypt

##genera un hash de prueba en el json de usuarios_prueba.json
#contraseña = "Admin123!"
#hash_generado = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
#print(hash_generado)


#Herramienta para leer json temporalmente
import json
import os

#Buscara la ruta del archivo usuarios_prueba.json en la carpeta backend
ruta_actual = os.path.dirname(__file__)
ruta_json = os.path.join(ruta_actual, "..", "usuarios_prueba.json")

with open(ruta_json, "r") as archivo:
    datos = json.load(archivo)

usuarios = datos["usuarios"]

#Definir qué datos recibe el login, si cooreo o contraseña no son str lo pasa
from pydantic import BaseModel

class LoginRequest(BaseModel):
    correo: str
    password: str

#El endpoint POST /login
@router.post("/login")
def login(datos_login: LoginRequest): #Recibimos los datos  de LoginRequest
    usuario_encontrado = None
    for usuario in usuarios: # buscamos el usuario en la lista de usuarios
        if usuario["correo"] == datos_login.correo:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None: #comparacion de contraseña, si no encuentra el usuario retorna un mensaje de error
        return { "codigo": 401, "mensaje": "usuario o contraseña incorrecto"}

    contraseña_correcta = bcrypt.checkpw(
        datos_login.password.encode(),
        usuario_encontrado["password"].encode()
    )

    if not contraseña_correcta:
        return {"codigo": 401, "mensaje": "Usuario o contraseña incorrectos"}

    return {
        "codigo": 200,
        "mensaje": "Login exitoso",
        "usuario": usuario_encontrado["usuario"],
        "rol": usuario_encontrado["rol"]
    }