from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioRol(str, Enum):
    ADMINISTRACION = "administracion"
    PROFESIONAL = "profesional"
    CAJERO = "cajero"
    AUDITOR = "auditor"

# Clase base con campos comunes
class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    rol: UsuarioRol = UsuarioRol.PROFESIONAL


    
# Schema para CREAR (lo que recibimos en el POST)
class UsuarioCreate(UsuarioBase):
    password: str # La contraseña es obligatoria al crear, pero no la devolvemos al leer

# Schema para RESPONDER (lo que devolvemos al cliente)
class UsuarioResponse(UsuarioBase):
    id: str
    estado: str
    fecha_creacion: datetime

    class Config:
        # Esto permite a Pydantic leer datos directamente de un objeto SQLAlchemy (ORM)
        from_attributes = True