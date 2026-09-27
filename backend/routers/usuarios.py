from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import bcrypt
from routers.auth import usuarios
from middleware.auth_middleware import requerir_rol

router = APIRouter(prefix="/usuarios", tags=["Usuarios y Roles"])

class UsuarioCreate(BaseModel):
    id: int
    usuario: str
    correo: str
    password: str
    rol: str
    activo: bool = True

class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

@router.get("/", dependencies=[Depends(requerir_rol(["administrador"]))])
def listar_usuarios():
    lista_limpia = []
    for u in usuarios:
        copia = u.copy()
        copia.pop("password", None)
        lista_limpia.append(copia)
    return lista_limpia

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(requerir_rol(["administrador"]))])
def crear_usuario(datos: UsuarioCreate):
    for u in usuarios:
        if u.get("correo") == datos.correo or u.get("id") == datos.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID o correo ya se encuentra registrado"
            )
    
    password_hash = bcrypt.hashpw(datos.password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    nuevo_usuario = {
        "id": datos.id,
        "usuario": datos.usuario,
        "correo": datos.correo,
        "password": password_hash,
        "rol": datos.rol,
        "activo": datos.activo
    }
    
    usuarios.append(nuevo_usuario)
    
    respuesta = nuevo_usuario.copy()
    respuesta.pop("password", None)
    return respuesta

@router.patch("/{usuario_id}", dependencies=[Depends(requerir_rol(["administrador"]))])
def actualizar_o_desactivar_usuario(usuario_id: int, datos: UsuarioUpdate):
    usuario_encontrado = None
    for u in usuarios:
        if u.get("id") == usuario_id:
            usuario_encontrado = u
            break
            
    if not usuario_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    cambios = datos.model_dump(exclude_unset=True)
    
    if "password" in cambios:
        cambios["password"] = bcrypt.hashpw(cambios["password"].encode(), bcrypt.gensalt()).decode('utf-8')
        
    usuario_encontrado.update(cambios)
    
    respuesta = usuario_encontrado.copy()
    respuesta.pop("password", None)
    return respuesta