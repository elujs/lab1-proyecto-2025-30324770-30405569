#En Clinico ira notas clinicas, diagnostico y consentimiento
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.episodio import EpisodioAtencion
from app.models.clinico import NotaClinica, Diagnostico, Consentimiento
from app.schemas.clinico_schema import NotaCreate, NotaResponse, DiagnosticoCreate, DiagnosticoResponse, ConsentimientoCreate, ConsentimientoResponse

router = APIRouter()

# --- NOTAS CLÍNICAS ---

@router.post("/episodios/{episodio_id}/notas", response_model=NotaResponse)
def crear_nota(episodio_id: str, nota: NotaCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el episodio exista
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=404, detail="Episodio no encontrado")
    
    # 2. Verificar si el episodio está cerrado (Regla implícita: no editar episodios cerrados)
    if episodio.estado == "cerrado":
        raise HTTPException(status_code=400, detail="No se pueden agregar notas a un episodio cerrado")

    # 3. Crear nota
    nueva_nota = NotaClinica(**nota.model_dump(), episodio_id=episodio_id)
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota

@router.get("/episodios/{episodio_id}/notas", response_model=List[NotaResponse])
def listar_notas(episodio_id: str, db: Session = Depends(get_db)):
    return db.query(NotaClinica).filter(NotaClinica.episodio_id == episodio_id).all()

# --- DIAGNÓSTICOS ---

@router.post("/episodios/{episodio_id}/diagnosticos", response_model=DiagnosticoResponse)
def agregar_diagnostico(episodio_id: str, diag: DiagnosticoCreate, db: Session = Depends(get_db)):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=404, detail="Episodio no encontrado")

    # Regla de negocio: Diagnóstico principal único por episodio (RF 6.3)
    if diag.principal:
        existe_principal = db.query(Diagnostico).filter(
            Diagnostico.episodio_id == episodio_id,
            Diagnostico.principal == True
        ).first()
        if existe_principal:
            raise HTTPException(status_code=400, detail="Ya existe un diagnóstico principal para este episodio")

    nuevo_diag = Diagnostico(**diag.model_dump(), episodio_id=episodio_id)
    db.add(nuevo_diag)
    db.commit()
    db.refresh(nuevo_diag)
    return nuevo_diag

@router.post("/episodios/{episodio_id}/consentimientos", response_model=ConsentimientoResponse)
def crear_consentimiento(episodio_id: str, consent: ConsentimientoCreate, db: Session = Depends(get_db)):
    # 1. Verificar episodio
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=404, detail="Episodio no encontrado")

    # 2. Crear consentimiento (Autocompletamos persona_id desde el episodio)
    nuevo_consent = Consentimiento(
        **consent.model_dump(),
        episodio_id=episodio_id,
        persona_id=episodio.persona_id
    )
    
    db.add(nuevo_consent)
    db.commit()
    db.refresh(nuevo_consent)
    return nuevo_consent

@router.get("/episodios/{episodio_id}/consentimientos", response_model=List[ConsentimientoResponse])
def listar_consentimientos(episodio_id: str, db: Session = Depends(get_db)):
    return db.query(Consentimiento).filter(Consentimiento.episodio_id == episodio_id).all()