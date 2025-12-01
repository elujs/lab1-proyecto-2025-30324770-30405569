from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UnidadTipo(str, Enum):
    SEDE = "sede"
    CONSULTORIO = "consultorio"
    SERVICIO = "servicio"
class UnidadBase(BaseModel):
    
    nombre: str
    tipo: UnidadTipo
    
    
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    horario_referencia: Optional[str] = None

class UnidadCreate(UnidadBase):
    pass

class UnidadUpdate(BaseModel):
   
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    horario_referencia: Optional[str] = None
    estado: Optional[str] = None # Para activación/desactivación

class UnidadResponse(UnidadBase):
    id: str
    estado: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True