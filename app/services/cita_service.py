from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cita import Cita
from app.models.agenda import Agenda
from app.schemas.cita_schema import CitaCreate, CitaUpdate

def create_cita(db: Session, cita: CitaCreate):
    # Regla: Debe existir agenda abierta
    agenda = db.query(Agenda).filter(
        Agenda.profesional_id == cita.profesional_id,
        Agenda.estado == "abierto",
        Agenda.fecha_inicio <= cita.fecha_hora_inicio,
        Agenda.fecha_fin >= cita.fecha_hora_fin
    ).first()

    if not agenda:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay agenda disponible")
    
    # Regla: Evitar solapamiento (409 Conflict)
    overlap = db.query(Cita).filter(
        Cita.profesional_id == cita.profesional_id,
        Cita.estado != "cancelada", 
        Cita.fecha_hora_inicio < cita.fecha_hora_fin,
        Cita.fecha_hora_fin > cita.fecha_hora_inicio
    ).first()

    if overlap:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El profesional ya tiene una cita en ese horario")

    new_cita = Cita(**cita.model_dump())
    db.add(new_cita)
    db.commit()
    db.refresh(new_cita)
    return new_cita

def update_cita(db: Session, cita_id: str, updates: CitaUpdate):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    cita.estado = updates.estado
    db.commit()
    db.refresh(cita)
    return cita