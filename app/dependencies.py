# app/dependencies.py

from fastapi import Depends, HTTPException, status
from app.services.auth_service import get_current_user_data
from app.schemas.auth_schema import TokenData

# --- Definición de Permisos (RBAC) ---

def requires_admin(user: TokenData = Depends(get_current_user_data)):
    if user.rol != "administracion":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Requiere rol de Administrador"
        )
    return user

def requires_clinico(user: TokenData = Depends(get_current_user_data)):

    if user.rol not in ["administracion", "profesional", "auditor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Requiere rol Clínico o Auditoría"
        )
    return user

def requires_identidad_creator(user: TokenData = Depends(get_current_user_data)):
    # Para crear Pacientes: Admins y Cajeros (Admisión)
    if user.rol not in ["administracion", "cajero"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Solo personal administrativo o cajeros pueden gestionar identidades."
        )
    return user

def requires_auth(user: TokenData = Depends(get_current_user_data)):
    # Solo requiere estar logueado (cualquier rol)
    return user