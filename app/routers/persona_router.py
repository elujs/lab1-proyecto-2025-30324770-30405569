from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.persona_schema import PersonaCreate, PersonaResponse, PersonaUpdate
from app.dependencies import requires_identidad_creator, requires_auth
from app.services import persona_service

router = APIRouter()

@router.post("/personas", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_identidad_creator)])
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    return persona_service.create_persona(db, persona)

@router.get("/personas/{persona_id}", response_model=PersonaResponse, dependencies=[Depends(requires_auth)])
def get_persona(persona_id: str, db: Session = Depends(get_db)):
    return persona_service.get_persona(db, persona_id)

@router.get("/personas", response_model=List[PersonaResponse], dependencies=[Depends(requires_auth)])
def list_personas(db: Session = Depends(get_db)):
    return persona_service.list_personas(db)

@router.patch("/personas/{persona_id}", response_model=PersonaResponse, dependencies=[Depends(requires_identidad_creator)])
def update_persona(persona_id: str, updates: PersonaUpdate, db: Session = Depends(get_db)):
    return persona_service.update_persona(db, persona_id, updates)

@router.delete("/personas/{persona_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(requires_identidad_creator)])
def delete_persona(persona_id: str, db: Session = Depends(get_db)):
    persona_service.delete_persona(db, persona_id)