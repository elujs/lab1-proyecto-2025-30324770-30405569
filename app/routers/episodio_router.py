from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.episodio_schema import EpisodioCreate, EpisodioResponse, EpisodioUpdate, EpisodioEstado
from app.dependencies import requires_clinico, requires_auth
from app.services import episodio_service 

router = APIRouter()

@router.post("/episodios", response_model=EpisodioResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_clinico)])
def create_episodio(episodio: EpisodioCreate, db: Session = Depends(get_db)):
    return episodio_service.create_episodio(db, episodio)

@router.get("/episodios", response_model=List[EpisodioResponse], dependencies=[Depends(requires_auth)])
def list_episodios(persona_id: str = None, estado: EpisodioEstado = None, db: Session = Depends(get_db)):
    return episodio_service.list_episodios(db, persona_id, estado)

@router.get("/episodios/{episodio_id}", response_model=EpisodioResponse, dependencies=[Depends(requires_auth)])
def get_episodio(episodio_id: str, db: Session = Depends(get_db)):
    return episodio_service.get_episodio(db, episodio_id)

@router.patch("/episodios/{episodio_id}", response_model=EpisodioResponse, dependencies=[Depends(requires_clinico)])
def update_episodio(episodio_id: str, updates: EpisodioUpdate, db: Session = Depends(get_db)):
    return episodio_service.update_episodio(db, episodio_id, updates)