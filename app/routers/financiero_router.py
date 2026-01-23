from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db

from app.models.cobertura import Aseguradora, PlanCobertura
from app.models.facturacion import Prestacion, Arancel, Factura, FacturaItem, Pago
from app.schemas.financiero_schema import (
    AseguradoraCreate, AseguradoraResponse, 
    PlanCreate, PlanResponse,
    PrestacionCreate, PrestacionResponse,
    FacturaCreate, FacturaResponse,
    PagoCreate
)
from app.dependencies import requires_admin, requires_auth 

router = APIRouter()



@router.post("/aseguradoras", response_model=AseguradoraResponse, dependencies=[Depends(requires_admin)])
def create_aseguradora(data: AseguradoraCreate, db: Session = Depends(get_db)):
    nueva = Aseguradora(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/aseguradoras", response_model=List[AseguradoraResponse], dependencies=[Depends(requires_auth)])
def list_aseguradoras(db: Session = Depends(get_db)):
    return db.query(Aseguradora).all()

@router.post("/planes", response_model=PlanResponse, dependencies=[Depends(requires_admin)])
def create_plan(data: PlanCreate, db: Session = Depends(get_db)):
    nuevo = PlanCobertura(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo



@router.post("/prestaciones", response_model=PrestacionResponse, dependencies=[Depends(requires_admin)])
def create_prestacion(data: PrestacionCreate, db: Session = Depends(get_db)):
    nueva = Prestacion(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva



@router.post("/facturas", response_model=FacturaResponse, dependencies=[Depends(requires_auth)])
def create_factura(data: FacturaCreate, db: Session = Depends(get_db)):
    
    total_factura = 0
    items_db = []
    
    
    count = db.query(Factura).count()
    nuevo_numero = f"FAC-{count + 1:06d}"

    nueva_factura = Factura(
        numero=nuevo_numero,
        persona_id=data.persona_id,
        aseguradora_id=data.aseguradora_id,
        estado="emitida"
    )
    db.add(nueva_factura)
    db.flush() 

    for item in data.items:
        subtotal = item.valor_unitario * item.cantidad
        total_factura += subtotal
        
        nuevo_item = FacturaItem(
            factura_id=nueva_factura.id,
            prestacion_codigo=item.prestacion_codigo,
            cantidad=item.cantidad,
            valor_unitario=item.valor_unitario,
            total_linea=subtotal
        )
        db.add(nuevo_item)

    nueva_factura.total = total_factura
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura

@router.post("/pagos", dependencies=[Depends(requires_auth)])
def registrar_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == pago.factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    
    pagos_previos = db.query(func.sum(Pago.monto)).filter(Pago.factura_id == factura.id).scalar() or 0
    saldo_pendiente = factura.total - pagos_previos

    if pago.monto > saldo_pendiente:
        raise HTTPException(status_code=400, detail=f"El monto excede el saldo pendiente ({saldo_pendiente})")

    nuevo_pago = Pago(**pago.model_dump())
    db.add(nuevo_pago)
    
    if (saldo_pendiente - pago.monto) == 0:
        factura.estado = "pagada"
        
    db.commit()
    return {"mensaje": "Pago registrado exitosamente", "nuevo_saldo": saldo_pendiente - pago.monto}