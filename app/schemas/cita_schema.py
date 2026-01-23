from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CitaBase(BaseModel):
    persona_id: str
    profesional_id: str
    unidad_id: str
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    motivo: Optional[str] = None
    canal: Optional[str] = "presencial"

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    estado: Optional[str] = None
    fecha_hora_inicio: Optional[datetime] = None 
    fecha_hora_fin: Optional[datetime] = None    
    observaciones: Optional[str] = None
    motivo_reprogramacion: Optional[str] = None 

class CitaResponse(CitaBase):
    id: str
    estado: str
    class Config:
        from_attributes = True

class CitaHistorialResponse(BaseModel):
    id: str
    estado_anterior: Optional[str]
    estado_nuevo: Optional[str]
    fecha_inicio_anterior: Optional[datetime]
    fecha_inicio_nueva: Optional[datetime]
    fecha_cambio: datetime
    motivo_cambio: Optional[str]

    class Config:
        from_attributes = True