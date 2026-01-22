from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.clinico_schema import NotaCreate, NotaResponse, DiagnosticoCreate, DiagnosticoResponse, ConsentimientoCreate, ConsentimientoResponse
from app.dependencies import requires_clinico, requires_auth
from app.services import clinico_service

router = APIRouter()

@router.post("/episodios/{episodio_id}/notas", response_model=NotaResponse, dependencies=[Depends(requires_clinico)])
def create_nota(episodio_id: str, nota: NotaCreate, db: Session = Depends(get_db)):
    return clinico_service.create_nota(db, episodio_id, nota)

@router.post("/episodios/{episodio_id}/diagnosticos", response_model=DiagnosticoResponse, dependencies=[Depends(requires_clinico)])
def add_diagnostico(episodio_id: str, diag: DiagnosticoCreate, db: Session = Depends(get_db)):
    return clinico_service.add_diagnostico(db, episodio_id, diag)

@router.post("/episodios/{episodio_id}/consentimientos", response_model=ConsentimientoResponse, dependencies=[Depends(requires_clinico)])
def create_consentimiento(episodio_id: str, consent: ConsentimientoCreate, db: Session = Depends(get_db)):
    return clinico_service.create_consentimiento(db, episodio_id, consent)