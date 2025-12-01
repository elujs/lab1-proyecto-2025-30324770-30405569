from sqlalchemy import Column, String, DateTime, ForeignKey, Text
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

    paciente = relationship("PersonaAtendida")
    profesional = relationship("Profesional")
    unidad = relationship("UnidadAtencion")