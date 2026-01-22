from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.episodio import EpisodioAtencion
from app.models.persona import PersonaAtendida
from app.schemas.episodio_schema import EpisodioCreate, EpisodioUpdate, EpisodioEstado

def create_episodio(db: Session, episodio: EpisodioCreate):
    # Regla MER: El paciente debe existir
    paciente = db.query(PersonaAtendida).filter(PersonaAtendida.id == episodio.persona_id).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")

    new_episodio = EpisodioAtencion(**episodio.model_dump())
    db.add(new_episodio)
    db.commit()
    db.refresh(new_episodio)
    return new_episodio

def list_episodios(db: Session, persona_id: str = None, estado: EpisodioEstado = None):
    query = db.query(EpisodioAtencion)
    if persona_id:
        query = query.filter(EpisodioAtencion.persona_id == persona_id)
    if estado:
        query = query.filter(EpisodioAtencion.estado == estado)
    return query.all()

def get_episodio(db: Session, episodio_id: str):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episodio no encontrado")
    return episodio

def update_episodio(db: Session, episodio_id: str, updates: EpisodioUpdate):
    episodio = get_episodio(db, episodio_id)
    
    # Regla: "Un episodio solo puede cerrarse si no existen órdenes en curso"
    # (Nota: Se implementará en la Sección 2.4 al tener el modelo de Órdenes)
    
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(episodio, key, value)
        
    db.commit()
    db.refresh(episodio)
    return episodio