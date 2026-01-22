from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.agenda import Agenda
from app.schemas.agenda_schema import AgendaCreate, AgendaUpdate

def create_agenda(db: Session, agenda: AgendaCreate):
    if agenda.fecha_inicio >= agenda.fecha_fin:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha de fin debe ser posterior al inicio.")

    new_block = Agenda(**agenda.model_dump())
    db.add(new_block)
    db.commit()
    db.refresh(new_block)
    return new_block

def list_agendas(db: Session, profesional_id: str = None, unidad_id: str = None, estado: str = None):
    query = db.query(Agenda)
    if profesional_id: query = query.filter(Agenda.profesional_id == profesional_id)
    if unidad_id: query = query.filter(Agenda.unidad_id == unidad_id)
    if estado: query = query.filter(Agenda.estado == estado)
    return query.all()

def update_agenda(db: Session, agenda_id: str, updates: AgendaUpdate):
    block = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bloque de agenda no encontrado")
    
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(block, key, value)
    db.commit()
    db.refresh(block)
    return block