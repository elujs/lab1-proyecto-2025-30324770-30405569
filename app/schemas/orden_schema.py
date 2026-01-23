from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrdenItem(BaseModel):
    codigo: str
    descripcion: str
    indicaciones: str

class OrdenBase(BaseModel):
    tipo: str
    prioridad: str = "normal"
    detalle: List[OrdenItem]

class OrdenCreate(OrdenBase):
    episodio_id: str

class OrdenResponse(OrdenBase):
    id: str
    episodio_id: str
    estado: str
    fecha_emision: datetime
    class Config: from_attributes = True

class PrescripcionItem(BaseModel):
    medicamentoCodigo: str
    nombre: str
    dosis: str
    via: str
    frecuencia: str
    duracion: str

class PrescripcionCreate(BaseModel):
    episodio_id: str
    items: List[PrescripcionItem]
    observaciones: Optional[str] = None

class ResultadoCreate(BaseModel):
    orden_id: str
    resumen: str
    archivo_id: Optional[str] = None