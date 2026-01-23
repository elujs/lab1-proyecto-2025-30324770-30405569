from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class AseguradoraBase(BaseModel):
    nombre: str
    nit: str
    contacto: Optional[str] = None

class AseguradoraCreate(AseguradoraBase):
    pass

class AseguradoraResponse(AseguradoraBase):
    id: str
    estado: str
    class Config:
        from_attributes = True

class PlanCreate(BaseModel):
    aseguradora_id: str
    nombre: str
    condiciones_generales: Optional[str] = None

class PlanResponse(PlanCreate):
    id: str
    class Config:
        from_attributes = True


class PrestacionCreate(BaseModel):
    codigo: str
    nombre: str
    grupo: Optional[str] = None

class PrestacionResponse(PrestacionCreate):
    class Config:
        from_attributes = True

class ArancelCreate(BaseModel):
    prestacion_codigo: str
    plan_id: Optional[str] = None 
    valor_base: Decimal
    vigente_desde: date

class FacturaItemCreate(BaseModel):
    prestacion_codigo: str
    cantidad: int = 1
    valor_unitario: Decimal

class FacturaCreate(BaseModel):
    persona_id: Optional[str] = None
    aseguradora_id: Optional[str] = None
    items: List[FacturaItemCreate]

class PagoCreate(BaseModel):
    factura_id: str
    monto: Decimal
    medio: str
    referencia: Optional[str] = None

class FacturaResponse(BaseModel):
    id: str
    numero: str
    total: Decimal
    estado: str
    fecha_emision: datetime
    class Config:
        from_attributes = True