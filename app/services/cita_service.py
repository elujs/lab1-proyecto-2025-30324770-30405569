from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cita import Cita, CitaHistorial
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

    # 1. SI HAY REPROGRAMACIÓN (Cambio de fechas)
    if updates.fecha_hora_inicio or updates.fecha_hora_fin:
        nueva_fecha_inicio = updates.fecha_hora_inicio or cita.fecha_hora_inicio
        nueva_fecha_fin = updates.fecha_hora_fin or cita.fecha_hora_fin

        # Validar nueva disponibilidad en agenda
        agenda = db.query(Agenda).filter(
            Agenda.profesional_id == cita.profesional_id,
            Agenda.estado == "abierto",
            Agenda.fecha_inicio <= nueva_fecha_inicio,
            Agenda.fecha_fin >= nueva_fecha_fin
        ).first()

        if not agenda:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay agenda disponible para el nuevo horario")

        # Validar solapamiento (excluyendo la misma cita que estamos editando)
        overlap = db.query(Cita).filter(
            Cita.profesional_id == cita.profesional_id,
            Cita.id != cita_id, # Ignorar esta misma cita
            Cita.estado != "cancelada",
            Cita.fecha_hora_inicio < nueva_fecha_fin,
            Cita.fecha_hora_fin > nueva_fecha_inicio
        ).first()

        if overlap:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflicto: El profesional ya tiene otra cita en ese horario")

    # 2. REGISTRAR EN HISTORIAL (Audit Log)
    historial = CitaHistorial(
        cita_id=cita_id,
        estado_anterior=cita.estado,
        estado_nuevo=updates.estado or cita.estado,
        fecha_inicio_anterior=cita.fecha_hora_inicio,
        fecha_inicio_nueva=updates.fecha_hora_inicio or cita.fecha_hora_inicio,
        motivo_cambio=updates.motivo_reprogramacion
    )
    db.add(historial)

    # 3. APLICAR CAMBIOS
    update_data = updates.model_dump(exclude_unset=True, exclude={"motivo_reprogramacion"})
    for key, value in update_data.items():
        setattr(cita, key, value)
    
    db.commit()
    db.refresh(cita)
    return cita