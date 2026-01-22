from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.agenda_schema import AgendaCreate, AgendaResponse, AgendaUpdate
from app.dependencies import requires_agendamiento, requires_auth 
from app.services import agenda_service

router = APIRouter()

@router.post("/agenda", response_model=AgendaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_agendamiento)])
def create_agenda(agenda: AgendaCreate, db: Session = Depends(get_db)):
    return agenda_service.create_agenda(db, agenda)

@router.get("/agenda", response_model=List[AgendaResponse], dependencies=[Depends(requires_auth)])
def get_agendas(profesional_id: Optional[str] = Query(None), unidad_id: Optional[str] = Query(None), estado: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return agenda_service.list_agendas(db, profesional_id, unidad_id, estado)

@router.patch("/agenda/{agenda_id}", response_model=AgendaResponse, dependencies=[Depends(requires_agendamiento)])
def update_agenda(agenda_id: str, updates: AgendaUpdate, db: Session = Depends(get_db)):
    return agenda_service.update_agenda(db, agenda_id, updates)