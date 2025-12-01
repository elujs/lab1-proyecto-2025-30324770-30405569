from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioRol(str, Enum):
    ADMINISTRACION = "administracion"
    PROFESIONAL = "profesional"
    CAJERO = "cajero"
    AUDITOR = "auditor"


class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    rol: UsuarioRol = UsuarioRol.PROFESIONAL


    

class UsuarioCreate(UsuarioBase):
    password: str # La contraseña es obligatoria al crear, pero no la devolvemos al leer


class UsuarioResponse(UsuarioBase):
    id: str
    estado: str
    fecha_creacion: datetime

    class Config:
        
        from_attributes = True