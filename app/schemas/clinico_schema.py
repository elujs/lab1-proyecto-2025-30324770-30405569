#En Clinico ira notas clinicas, diagnostico y consentimiento

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Diagnósticos 
class TipoDiagnostico(str, Enum):
    PRESUNTIVO = "presuntivo"
    DEFINITIVO = "definitivo"


class DiagnosticoBase(BaseModel):
    codigo: str
    descripcion: str
    tipo: TipoDiagnostico
    principal: bool = False

class DiagnosticoCreate(DiagnosticoBase):
    pass

class DiagnosticoResponse(DiagnosticoBase):
    id: str
    class Config:
        from_attributes = True

# Notas Clínicas 
class NotaBase(BaseModel):
    profesional_id: str
    subjetivo: str
    objetivo: str
    analisis: str
    plan: str

class NotaCreate(NotaBase):
    pass

class NotaResponse(NotaBase):
    id: str
    fecha: datetime
    version: str
    class Config:
        from_attributes = True


# Consentimiento
class MetodoConsentimiento(str, Enum):
    DIGITAL = "firma_digital"
    VERBAL = "aceptacion_verbal"

class ConsentimientoBase(BaseModel):
    tipo_procedimiento: str
    metodo: MetodoConsentimiento
    archivo_id: Optional[str] = None

class ConsentimientoCreate(ConsentimientoBase):
    pass

class ConsentimientoResponse(ConsentimientoBase):
    id: str
    persona_id: str
    episodio_id: str
    fecha: datetime
    
    class Config:
        from_attributes = True