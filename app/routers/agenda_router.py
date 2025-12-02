from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.agenda import Agenda
from app.schemas.agenda_schema import AgendaCreate, AgendaResponse, AgendaUpdate
# Importamos las dependencias de seguridad
from app.dependencies import requires_admin, requires_agendamiento, requires_auth 

router = APIRouter()

# 1. POST /agenda: Crear bloque (Restringido a Admin o quien tenga rol de agendamiento/profesional)
# Asumimos que un profesional puede crear su propia agenda, o un admin.
@router.post(
    "/agenda", 
    response_model=AgendaResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requires_agendamiento)] # <-- SEGURIDAD APLICADA
)
def create_agenda(agenda: AgendaCreate, db: Session = Depends(get_db)):
    if agenda.fecha_inicio >= agenda.fecha_fin:
         raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior al inicio.")

    nuevo_bloque = Agenda(**agenda.model_dump())
    db.add(nuevo_bloque)
    db.commit()
    db.refresh(nuevo_bloque)
    return nuevo_bloque

# 2. GET /agenda: Listar (Abierto a cualquier usuario autenticado para ver disponibilidad)
@router.get(
    "/agenda", 
    response_model=List[AgendaResponse],
    dependencies=[Depends(requires_auth)] # <-- SEGURIDAD APLICADA (Solo login)
)
def get_agendas(
    profesional_id: Optional[str] = Query(None),
    unidad_id: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Agenda)
    if profesional_id:
        query = query.filter(Agenda.profesional_id == profesional_id)
    if unidad_id:
        query = query.filter(Agenda.unidad_id == unidad_id)
    if estado:
        query = query.filter(Agenda.estado == estado)
    return query.all()

# 3. PATCH /agenda: Modificar (Restringido igual que crear)
@router.patch(
    "/agenda/{agenda_id}", 
    response_model=AgendaResponse,
    dependencies=[Depends(requires_agendamiento)] # <-- SEGURIDAD APLICADA
)
def update_agenda(agenda_id: str, updates: AgendaUpdate, db: Session = Depends(get_db)):
    bloque = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    if not bloque:
        raise HTTPException(status_code=404, detail="Bloque de agenda no encontrado")
        
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(bloque, key, value)
        
    db.commit()
    db.refresh(bloque)
    return bloque