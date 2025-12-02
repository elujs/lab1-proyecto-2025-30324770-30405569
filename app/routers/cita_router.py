from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.cita import Cita
from app.models.agenda import Agenda
from app.schemas.cita_schema import CitaCreate, CitaResponse, CitaUpdate
# Importamos seguridad
from app.dependencies import requires_agendamiento, requires_auth

router = APIRouter()

# 1. POST /citas (Crear cita)
@router.post(
    "/citas", 
    response_model=CitaResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requires_agendamiento)] # <-- Solo personal autorizado agenda
)
def create_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    # Validar agenda (Regla de Negocio: Agenda abierta y fechas coincidentes)
    #faltan validaciones. 
    agenda = db.query(Agenda).filter(
        Agenda.profesional_id == cita.profesional_id,
        Agenda.unidad_id == cita.unidad_id,
        Agenda.estado == "abierto",
        Agenda.fecha_inicio <= cita.fecha_hora_inicio,
        Agenda.fecha_fin >= cita.fecha_hora_fin
    ).first()

    if not agenda:
        raise HTTPException(status_code=400, detail="No hay agenda disponible o cerrada para este horario")

    nueva_cita = Cita(**cita.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

# 2. GET /citas (Ver citas)
@router.get(
    "/citas", 
    response_model=List[CitaResponse],
    dependencies=[Depends(requires_auth)] # <-- Cualquier empleado logueado puede verlas (o podrías restringirlo más)
)
def get_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()

# 3. PATCH /citas (Cancelar/Confirmar)
@router.patch(
    "/citas/{cita_id}", 
    response_model=CitaResponse,
    dependencies=[Depends(requires_agendamiento)] # <-- Requiere permisos de gestión
)
def update_cita(cita_id: str, updates: CitaUpdate, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    cita.estado = updates.estado
    db.commit()
    db.refresh(cita)
    return cita