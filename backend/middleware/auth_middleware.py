from fastapi import Depends, HTTPException, status, Header
from routers.auth import usuarios


def obtener_usuario_actual(x_usuario_correo: str = Header(...)): #Obtiene el usuario por medio de HTTP y lo guarda
    for u in usuarios:
        if u.get("correo") == x_usuario_correo:  #Obtiene el usuario, lo compara con lo que están en la lista usuarios
            return u
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  #Si hay un error muestra el estado HTTP 401
        detail="Usuario no autenticado o no encontrado"
    )

def requerir_rol(roles_permitidos: list[str]): #recibe un parámetro tipo lista de los roles permitidos
    def verificacion(usuario_actual: dict = Depends(obtener_usuario_actual)): #Obtiene la varaible de la función de arriba
        if not usuario_actual.get("activo", True):  #verifica si el usuario está activo
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="El usuario se encuentra inactivo"
            )
        
        if usuario_actual.get("rol") not in roles_permitidos: #Compara si el usuario actual tiene permiso para ingresar
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos necesarios para realizar esta acción"
            )
        
        return usuario_actual

    return verificacion