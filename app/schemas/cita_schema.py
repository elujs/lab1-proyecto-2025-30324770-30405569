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
    estado: str

class CitaResponse(CitaBase):
    id: str
    estado: str
    class Config:
        from_attributes = True