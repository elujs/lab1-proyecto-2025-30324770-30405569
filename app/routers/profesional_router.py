# app/routers/profesional_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.profesional import Profesional
from app.schemas.profesional_schema import ProfesionalCreate, ProfesionalResponse, ProfesionalUpdate
from typing import List
from app.dependencies import requires_admin, requires_auth

router = APIRouter()

@router.post(
    "/profesionales", 
    response_model=ProfesionalResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requires_admin)] # <-- Solo Admin
)
def create_profesional(profesional: ProfesionalCreate, db: Session = Depends(get_db)):
    registro_existente = db.query(Profesional).filter(
        Profesional.registro_profesional == profesional.registro_profesional
    ).first()
    
    if registro_existente:
        raise HTTPException(status_code=409, detail="Registro profesional ya existe.")

    nuevo_profesional = Profesional(**profesional.model_dump())
    db.add(nuevo_profesional)
    db.commit()
    db.refresh(nuevo_profesional) 
    return nuevo_profesional

@router.get(
    "/profesionales/{profesional_id}", 
    response_model=ProfesionalResponse,
    dependencies=[Depends(requires_auth)]
)
def get_profesional(profesional_id: str, db: Session = Depends(get_db)):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    if not profesional:
        raise HTTPException(status_code=404, detail="Profesional no encontrado.")
    return profesional

@router.get(
    "/profesionales", 
    response_model=List[ProfesionalResponse],
    dependencies=[Depends(requires_auth)]
)
def list_profesionales(db: Session = Depends(get_db)):
    return db.query(Profesional).all()

@router.patch(
    "/profesionales/{profesional_id}", 
    response_model=ProfesionalResponse,
    dependencies=[Depends(requires_admin)] # <-- Solo Admin
)
def update_profesional(profesional_id: str, updates: ProfesionalUpdate, db: Session = Depends(get_db)):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    if not profesional:
        raise HTTPException(status_code=404, detail="Profesional no encontrado.")

    update_data = updates.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(profesional, key, value)
    
    db.add(profesional)
    db.commit()
    db.refresh(profesional)
    return profesional

@router.delete(
    "/profesionales/{profesional_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(requires_admin)] # <-- Solo Admin
)
def delete_profesional(profesional_id: str, db: Session = Depends(get_db)):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    if not profesional:
        raise HTTPException(status_code=404, detail="Profesional no encontrado.")

    profesional.estado = "inactivo" 
    db.add(profesional)
    db.commit()
    return