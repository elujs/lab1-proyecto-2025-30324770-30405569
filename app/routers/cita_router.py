from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cita_schema import CitaCreate, CitaResponse, CitaUpdate
from app.dependencies import requires_agendamiento, requires_auth
from app.services import cita_service

router = APIRouter()

@router.post("/citas", response_model=CitaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_agendamiento)])
def create_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    return cita_service.create_cita(db, cita)

@router.get("/citas", response_model=List[CitaResponse], dependencies=[Depends(requires_auth)])
def get_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()

@router.patch("/citas/{cita_id}", response_model=CitaResponse, dependencies=[Depends(requires_agendamiento)])
def update_cita(cita_id: str, updates: CitaUpdate, db: Session = Depends(get_db)):
    return cita_service.update_cita(db, cita_id, updates)