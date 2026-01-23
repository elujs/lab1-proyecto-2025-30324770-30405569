from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.episodio import EpisodioAtencion
from app.models.persona import PersonaAtendida
from app.schemas.episodio_schema import EpisodioCreate, EpisodioUpdate, EpisodioEstado
from app.models.orden import Orden

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
    
    # REGLA RF 6.2: No cerrar si hay órdenes pendientes
    if updates.estado == "cerrado":
        ordenes_activas = db.query(Orden).filter(
            Orden.episodio_id == episodio_id,
            Orden.estado.in_(["emitida", "autorizada", "enCurso"])
        ).count()
        
        if ordenes_activas > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"No se puede cerrar: el episodio tiene {ordenes_activas} órdenes en curso."
            )
            
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(episodio, key, value)
        
    db.commit()
    db.refresh(episodio)
    return episodio