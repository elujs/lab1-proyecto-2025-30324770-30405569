from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.profesional_schema import ProfesionalCreate, ProfesionalResponse, ProfesionalUpdate
from app.dependencies import requires_admin, requires_auth
from app.services import profesional_service

router = APIRouter()

@router.post("/profesionales", response_model=ProfesionalResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_admin)])
def create_profesional(profesional: ProfesionalCreate, db: Session = Depends(get_db)):
    return profesional_service.create_profesional(db, profesional)

@router.get("/profesionales/{profesional_id}", response_model=ProfesionalResponse, dependencies=[Depends(requires_auth)])
def get_profesional(profesional_id: str, db: Session = Depends(get_db)):
    return profesional_service.get_profesional(db, profesional_id)

@router.get("/profesionales", response_model=List[ProfesionalResponse], dependencies=[Depends(requires_auth)])
def list_profesionales(db: Session = Depends(get_db)):
    return profesional_service.list_profesionales(db)

@router.patch("/profesionales/{profesional_id}", response_model=ProfesionalResponse, dependencies=[Depends(requires_admin)])
def update_profesional(profesional_id: str, updates: ProfesionalUpdate, db: Session = Depends(get_db)):
    return profesional_service.update_profesional(db, profesional_id, updates)

@router.delete("/profesionales/{profesional_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(requires_admin)])
def delete_profesional(profesional_id: str, db: Session = Depends(get_db)):
    profesional_service.delete_profesional(db, profesional_id)