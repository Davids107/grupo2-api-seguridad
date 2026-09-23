from fastapi import APIRouter
router = APIRouter()

import bcrypt

#contraseña = "Admin123!"
#hash_generado = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
#print(hash_generado)

import json
import os

ruta_actual = os.path.dirname(__file__)
ruta_json = os.path.join(ruta_actual, "..", "usuarios_prueba.json")

with open(ruta_json, "r") as archivo:
    datos = json.load(archivo)

usuarios = datos["usuarios"]

from pydantic import BaseModel

class LoginRequest(BaseModel):
    correo: str
    password: str

@router.post("/login")
def login(datos_login: LoginRequest):
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario["correo"] == datos_login.correo:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
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