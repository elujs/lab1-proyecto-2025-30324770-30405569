from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgendaBase(BaseModel):
    profesional_id: str
    unidad_id: str
    fecha_inicio: datetime
    fecha_fin: datetime
    capacidad: Optional[int] = 1
    estado: Optional[str] = "abierto"

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(BaseModel):
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None

class AgendaResponse(AgendaBase):
    id: str

    class Config:
        from_attributes = True