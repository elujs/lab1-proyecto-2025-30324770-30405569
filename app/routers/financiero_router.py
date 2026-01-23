from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.financiero_schema import (
    AseguradoraCreate, AseguradoraResponse, 
    PlanCreate, PlanResponse,
    PrestacionCreate, PrestacionResponse,
    FacturaCreate, FacturaResponse,
    PagoCreate
)
from app.models.cobertura import Aseguradora
from app.dependencies import requires_admin, requires_auth
from app.services import financiero_service

router = APIRouter(prefix="/financiero", tags=["Financiero y Cobertura"])

@router.post("/aseguradoras", response_model=AseguradoraResponse, dependencies=[Depends(requires_admin)])
def create_aseguradora(data: AseguradoraCreate, db: Session = Depends(get_db)):
    return financiero_service.create_aseguradora(db, data)

@router.get("/aseguradoras", response_model=List[AseguradoraResponse], dependencies=[Depends(requires_auth)])
def list_aseguradoras(db: Session = Depends(get_db)):
    return db.query(Aseguradora).all()

@router.post("/planes", response_model=PlanResponse, dependencies=[Depends(requires_admin)])
def create_plan(data: PlanCreate, db: Session = Depends(get_db)):
    return financiero_service.create_plan(db, data)

@router.post("/prestaciones", response_model=PrestacionResponse, dependencies=[Depends(requires_admin)])
def create_prestacion(data: PrestacionCreate, db: Session = Depends(get_db)):
    return financiero_service.create_prestacion(db, data)

@router.post("/facturas", response_model=FacturaResponse, dependencies=[Depends(requires_auth)])
def create_factura(data: FacturaCreate, db: Session = Depends(get_db)):
    return financiero_service.create_factura(db, data)

@router.post("/pagos", dependencies=[Depends(requires_auth)])
def registrar_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    return financiero_service.registrar_pago(db, pago)