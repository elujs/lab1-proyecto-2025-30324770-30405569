from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.orden_schema import OrdenCreate, OrdenResponse, PrescripcionCreate, ResultadoCreate
from app.dependencies import requires_clinico
from app.services import orden_service

router = APIRouter(tags=["Órdenes y Prestaciones"])

@router.post("/ordenes", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_clinico)])
def emitir_orden(data: OrdenCreate, db: Session = Depends(get_db)):
    return orden_service.emitir_orden(db, data)

@router.post("/prescripciones", status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_clinico)])
def emitir_prescripcion(data: PrescripcionCreate, db: Session = Depends(get_db)):
    return orden_service.emitir_prescripcion(db, data)

@router.post("/resultados", dependencies=[Depends(requires_clinico)])
def registrar_resultado(data: ResultadoCreate, db: Session = Depends(get_db)):
    return orden_service.registrar_resultado(db, data)