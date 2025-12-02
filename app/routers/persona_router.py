# app/routers/persona_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.persona import PersonaAtendida
from app.schemas.persona_schema import PersonaCreate, PersonaResponse, PersonaUpdate
from typing import List
# Importamos seguridad
from app.dependencies import requires_identidad_creator, requires_auth

router = APIRouter()

# 1. POST /personas (Solo Admin/Cajero)
@router.post(
    "/personas", 
    response_model=PersonaResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requires_identidad_creator)]
)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    documento_existente = db.query(PersonaAtendida).filter(
        PersonaAtendida.numero_documento == persona.numero_documento
    ).first()
    
    if documento_existente:
        raise HTTPException(status_code=409, detail="El documento ya existe.")

    nueva_persona = PersonaAtendida(**persona.model_dump())
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona) 
    return nueva_persona

# 2. GET /personas/{id} (Cualquier usuario autenticado)
@router.get(
    "/personas/{persona_id}", 
    response_model=PersonaResponse,
    dependencies=[Depends(requires_auth)]
)
def get_persona(persona_id: str, db: Session = Depends(get_db)):
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
    return persona

# 3. GET /personas (Cualquier usuario autenticado)
@router.get(
    "/personas", 
    response_model=List[PersonaResponse],
    dependencies=[Depends(requires_auth)]
)
def list_personas(db: Session = Depends(get_db)):
    return db.query(PersonaAtendida).all()

# 4. PATCH (Solo Admin/Cajero)
@router.patch(
    "/personas/{persona_id}", 
    response_model=PersonaResponse,
    dependencies=[Depends(requires_identidad_creator)]
)
def update_persona(persona_id: str, updates: PersonaUpdate, db: Session = Depends(get_db)):
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")

    update_data = updates.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(persona, key, value)
    
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona

# 5. DELETE (Solo Admin/Cajero)
@router.delete(
    "/personas/{persona_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(requires_identidad_creator)]
)
def delete_persona(persona_id: str, db: Session = Depends(get_db)):
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")

    persona.estado = "inactivo" 
    db.add(persona)
    db.commit()
    return