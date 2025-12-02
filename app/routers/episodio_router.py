from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.episodio import EpisodioAtencion
from app.models.persona import PersonaAtendida
from app.schemas.episodio_schema import EpisodioCreate, EpisodioResponse, EpisodioUpdate, EpisodioEstado

router = APIRouter()

# 1. POST /episodios: Abrir un nuevo episodio
@router.post("/episodios", response_model=EpisodioResponse, status_code=status.HTTP_201_CREATED)
def create_episodio(episodio: EpisodioCreate, db: Session = Depends(get_db)):
    # Validar que el paciente exista
    paciente = db.query(PersonaAtendida).filter(PersonaAtendida.id == episodio.persona_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    nuevo_episodio = EpisodioAtencion(**episodio.model_dump())
    db.add(nuevo_episodio)
    db.commit()
    db.refresh(nuevo_episodio)
    return nuevo_episodio

# 2. GET /episodios: Listar episodios 
@router.get("/episodios", response_model=List[EpisodioResponse])
def list_episodios(persona_id: str = None, estado: EpisodioEstado = None, db: Session = Depends(get_db)):
    query = db.query(EpisodioAtencion)
    
    if persona_id:
        query = query.filter(EpisodioAtencion.persona_id == persona_id)
    if estado:
        query = query.filter(EpisodioAtencion.estado == estado)
        
    return query.all()

# 3. GET /episodios/{id}
@router.get("/episodios/{episodio_id}", response_model=EpisodioResponse)
def get_episodio(episodio_id: str, db: Session = Depends(get_db)):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=404, detail="Episodio no encontrado")
    return episodio

# 4. PATCH /episodios/{id}: Cerrar episodio o editar motivo
@router.patch("/episodios/{episodio_id}", response_model=EpisodioResponse)
def update_episodio(episodio_id: str, updates: EpisodioUpdate, db: Session = Depends(get_db)):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == episodio_id).first()
    if not episodio:
        raise HTTPException(status_code=404, detail="Episodio no encontrado")
        
  
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(episodio, key, value)
        
    db.commit()
    db.refresh(episodio)
    return episodio