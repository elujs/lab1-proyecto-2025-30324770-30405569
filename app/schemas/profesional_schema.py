from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProfesionalCategoria(str, Enum):
    MEDICO = "medico"
    ENFERMERIA = "enfermeria"
    TERAPIAS = "terapias"
class ProfesionalBase(BaseModel):
    
    nombres: str
    apellidos: str
    registro_profesional: str
    especialidad: str
    categoria: ProfesionalCategoria
    
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    agenda_habilitada: Optional[bool] = True

class ProfesionalCreate(ProfesionalBase):
    pass

class ProfesionalUpdate(BaseModel):
    # Campos que se permiten actualizar (todos opcionales para PATCH)
    categoria: Optional[ProfesionalCategoria]
    especialidad: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    agenda_habilitada: Optional[bool] = None
    estado: Optional[str] = None

class ProfesionalResponse(ProfesionalBase):
    id: str
    estado: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True