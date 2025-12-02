from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import uuid

class EpisodioAtencion(Base):
    __tablename__ = "episodios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    persona_id = Column(String, ForeignKey("personas_atendidas.id"), nullable=False)
    
    # Datos del episodio
    fecha_apertura = Column(DateTime(timezone=True), server_default=func.now())
    motivo = Column(Text, nullable=False)
    
    # Tipos: consulta, procedimiento, control, urgencia 
    tipo = Column(String, nullable=False)
    
    # Estado: abierto/cerrado
    estado = Column(String, default="abierto") 

    # Relaciones
    paciente = relationship("PersonaAtendida")