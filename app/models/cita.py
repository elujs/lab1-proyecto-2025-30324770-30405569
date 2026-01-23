from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Cita(Base):
    __tablename__ = "citas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    persona_id = Column(String, ForeignKey("personas_atendidas.id"), nullable=False)
    profesional_id = Column(String, ForeignKey("profesionales.id"), nullable=False)
    unidad_id = Column(String, ForeignKey("unidades_atencion.id"), nullable=False)
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=False)
    motivo = Column(Text, nullable=True)
    estado = Column(String, default="solicitada") 
    canal = Column(String, default="presencial")
    observaciones = Column(Text)


    paciente = relationship("PersonaAtendida")
    profesional = relationship("Profesional")
    unidad = relationship("UnidadAtencion")
    historial = relationship("CitaHistorial", back_populates="cita")

class CitaHistorial(Base):
    __tablename__ = "cita_historial"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cita_id = Column(String, ForeignKey("citas.id"), nullable=False)
    estado_anterior = Column(String)
    estado_nuevo = Column(String)
    fecha_inicio_anterior = Column(DateTime(timezone=True))
    fecha_inicio_nueva = Column(DateTime(timezone=True))
    fecha_cambio = Column(DateTime(timezone=True), server_default=func.now())
    motivo_cambio = Column(String)

    cita = relationship("Cita", back_populates="historial")