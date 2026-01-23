from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from decimal import Decimal
from app.models.cobertura import PlanCobertura, Aseguradora
from app.models.facturacion import Prestacion, Factura, FacturaItem, Pago
from app.schemas.financiero_schema import AseguradoraCreate, PlanCreate, PrestacionCreate, FacturaCreate, PagoCreate

def create_aseguradora(db: Session, data: AseguradoraCreate):
    nueva = Aseguradora(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def create_plan(db: Session, data: PlanCreate):
    nuevo = PlanCobertura(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def create_prestacion(db: Session, data: PrestacionCreate):
    nueva = Prestacion(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def create_factura(db: Session, data: FacturaCreate):
    total_factura = Decimal("0.00")
    
    # Generación de número correlativo automático
    count = db.query(Factura).count()
    nuevo_numero = f"FAC-{count + 1:06d}"

    nueva_factura = Factura(
        numero=nuevo_numero,
        persona_id=data.persona_id,
        aseguradora_id=data.aseguradora_id,
        estado="emitida"
    )
    db.add(nueva_factura)
    db.flush()  # Para obtener el ID generado de la factura antes del commit

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

def registrar_pago(db: Session, pago: PagoCreate):
    factura = db.query(Factura).filter(Factura.id == pago.factura_id).first()
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")

    # Cálculo del saldo pendiente sumando pagos anteriores
    pagos_previos = db.query(func.sum(Pago.monto)).filter(Pago.factura_id == factura.id).scalar() or 0
    saldo_pendiente = factura.total - Decimal(str(pagos_previos))

    if pago.monto > saldo_pendiente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El monto excede el saldo pendiente ({saldo_pendiente})"
        )

    nuevo_pago = Pago(**pago.model_dump())
    db.add(nuevo_pago)
    
    # Si el saldo queda en cero, la factura pasa a estado 'pagada'
    if (saldo_pendiente - pago.monto) == 0:
        factura.estado = "pagada"
        
    db.commit()
    return {"mensaje": "Pago registrado exitosamente", "nuevo_saldo": float(saldo_pendiente - pago.monto)}