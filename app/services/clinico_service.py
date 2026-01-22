from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.episodio import EpisodioAtencion
from app.models.clinico import NotaClinica, Diagnostico, Consentimiento
from app.schemas.clinico_schema import NotaCreate, DiagnosticoCreate, ConsentimientoCreate

def create_nota(db: Session, episodio_id: str, nota: NotaCreate):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio or episodio.estado == "cerrado":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Episodio no disponible")
    
    new_nota = NotaClinica(**nota.model_dump(), episodio_id=episodio_id)
    db.add(new_nota)
    db.commit()
    db.refresh(new_nota)
    return new_nota

def add_diagnostico(db: Session, episodio_id: str, diag: DiagnosticoCreate):
    if diag.principal:
        exists = db.query(Diagnostico).filter(Diagnostico.episodio_id == episodio_id, Diagnostico.principal == True).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un diagnóstico principal")

    new_diag = Diagnostico(**diag.model_dump(), episodio_id=episodio_id)
    db.add(new_diag)
    db.commit()
    db.refresh(new_diag)
    return new_diag

def create_consentimiento(db: Session, episodio_id: str, consent: ConsentimientoCreate):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episodio no encontrado")
    
    new_consent = Consentimiento(**consent.model_dump(), episodio_id=episodio_id, persona_id=episodio.persona_id)
    db.add(new_consent)
    db.commit()
    db.refresh(new_consent)
    return new_consent