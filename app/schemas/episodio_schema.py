from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EpisodioTipo(str, Enum):
    CONSULTA = "consulta"
    PROCEDIMIENTO = "procedimiento"
    CONTROL = "control"
    URGENCIA = "urgencia"

class EpisodioEstado(str, Enum):
    ABIERTO = "abierto"
    CERRADO = "cerrado"

class EpisodioBase(BaseModel):
    persona_id: str
    motivo: str
    tipo: EpisodioTipo
    estado: Optional[EpisodioEstado] = EpisodioEstado.ABIERTO

class EpisodioCreate(EpisodioBase):
    pass

class EpisodioUpdate(BaseModel):
    motivo: Optional[str] = None
    tipo: Optional[EpisodioTipo] = None
    estado: Optional[EpisodioEstado] = None 

class EpisodioResponse(EpisodioBase):
    id: str
    fecha_apertura: datetime

    class Config:
        from_attributes = True