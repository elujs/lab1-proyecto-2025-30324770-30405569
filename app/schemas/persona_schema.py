from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

# Base: Campos Comunes y de Lectura (Read Only)
class PersonaBase(BaseModel):
    
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    sexo: str
    
   
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = None

    
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None



class PersonaCreate(PersonaBase):
    
    pass



class PersonaUpdate(BaseModel):
    
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contacto_emergencia: Optional[str] = None
    alergias: Optional[str] = None
    antecedentes_resumen: Optional[str] = None
    estado: Optional[str] = None # Para la eliminación lógica



class PersonaResponse(PersonaBase):
    
    id: str
    estado: str
    fecha_creacion: datetime

    class Config:
        
        from_attributes = True