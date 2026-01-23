from sqlalchemy import Column, String, DateTime, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Aseguradora(Base):
    __tablename__ = "aseguradoras"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)
    nit = Column(String, unique=True, nullable=False)
    contacto = Column(String)
    estado = Column(String, default="activo") # activo/inactivo

class PlanCobertura(Base):
    __tablename__ = "planes_cobertura"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    aseguradora_id = Column(String, ForeignKey("aseguradoras.id"), nullable=False)
    nombre = Column(String, nullable=False)
    condiciones_generales = Column(String)
    
    aseguradora = relationship("Aseguradora", backref="planes")

class Afiliacion(Base):
    __tablename__ = "afiliaciones"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    persona_id = Column(String, ForeignKey("personas_atendidas.id"), nullable=False)
    plan_id = Column(String, ForeignKey("planes_cobertura.id"), nullable=False)
    
    numero_poliza = Column(String, nullable=False)
    vigente_desde = Column(Date, nullable=False)
    vigente_hasta = Column(Date, nullable=False)
    
    # Valores específicos del paciente en este plan
    copago = Column(Numeric(10, 2), default=0.00)
    cuota_moderadora = Column(Numeric(10, 2), default=0.00)
    
    paciente = relationship("PersonaAtendida")
    plan = relationship("PlanCobertura")