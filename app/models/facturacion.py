from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import uuid


class Prestacion(Base):
    __tablename__ = "prestaciones"
    nombre = Column(String, nullable=False)
    grupo = Column(String) 
    tiempo_estimado = Column(Integer) 

class Arancel(Base):
    __tablename__ = "aranceles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prestacion_codigo = Column(String, ForeignKey("prestaciones.codigo"), nullable=False)
    plan_id = Column(String, ForeignKey("planes_cobertura.id"), nullable=True) 
    
    valor_base = Column(Numeric(12, 2), nullable=False)
    impuestos = Column(Numeric(5, 2), default=0.00) 
    vigente_desde = Column(Date, nullable=False)
    vigente_hasta = Column(Date)


class Factura(Base):
    __tablename__ = "facturas"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    numero = Column(String, unique=True, nullable=False) 
    fecha_emision = Column(DateTime(timezone=True), server_default=func.now())
    
    
    persona_id = Column(String, ForeignKey("personas_atendidas.id"), nullable=True)
    aseguradora_id = Column(String, ForeignKey("aseguradoras.id"), nullable=True)
    
    total = Column(Numeric(12, 2), default=0.00)
    estado = Column(String, default="emitida") 
    
    items = relationship("FacturaItem", backref="factura")
    pagos = relationship("Pago", backref="factura")

class FacturaItem(Base):
    __tablename__ = "factura_items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    factura_id = Column(String, ForeignKey("facturas.id"), nullable=False)
    prestacion_codigo = Column(String, ForeignKey("prestaciones.codigo"), nullable=False)
    
    cantidad = Column(Integer, default=1)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    total_linea = Column(Numeric(12, 2), nullable=False)

class Pago(Base):
    __tablename__ = "pagos"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    factura_id = Column(String, ForeignKey("facturas.id"), nullable=False)
    
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    monto = Column(Numeric(12, 2), nullable=False)
    medio = Column(String, nullable=False) 
    referencia = Column(String) 