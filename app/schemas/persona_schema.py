from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

# Base: Campos Comunes y de Lectura (Read Only)
class PersonaBase(BaseModel):
    # Datos Mínimos (RF 2.1)
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    sexo: str
    
    # Contacto
    correo: EmailStr = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = None

    # Opcionales
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None


# Create: Para crear un nuevo paciente (POST)
class PersonaCreate(PersonaBase):
    # Hereda todos los campos obligatorios de PersonaBase
    pass


# Update: Para actualizar parcialmente (PATCH)
class PersonaUpdate(BaseModel):
    # Solo permitimos actualizar los campos que no son de identidad
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = None
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None
    estado: Optional[str] = None # Para la eliminación lógica


# Response: Lo que el cliente ve (GET, POST Response)
class PersonaResponse(PersonaBase):
    # Agrega los campos que son generados por la BD
    id: str
    estado: str
    fecha_creacion: datetime

    class Config:
        # Permite mapear los objetos de SQLAlchemy a Pydantic
        from_attributes = True