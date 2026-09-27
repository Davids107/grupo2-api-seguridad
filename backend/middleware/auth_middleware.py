from fastapi import Depends, HTTPException, status, Header
from routers.auth import usuarios

def obtener_usuario_actual(x_usuario_correo: str = Header(...)):
    for u in usuarios:
        if u.get("correo") == x_usuario_correo:
            return u
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario no autenticado o no encontrado"
    )

def requerir_rol(roles_permitidos: list[str]):
    def verificacion(usuario_actual: dict = Depends(obtener_usuario_actual)):
        if not usuario_actual.get("activo", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario se encuentra inactivo"
            )
        
        if usuario_actual.get("rol") not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos necesarios para realizar esta acción"
            )
        
        return usuario_actual

    return verificacion