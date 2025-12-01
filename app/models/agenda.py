from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
   
    profesional_id = Column(String, ForeignKey("profesionales.id"), nullable=False)
    unidad_id = Column(String, ForeignKey("unidades_atencion.id"), nullable=False)
    
    
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    
   
    capacidad = Column(Integer, default=1)
    estado = Column(String, default="abierto")
    profesional = relationship("Profesional")
    unidad = relationship("UnidadAtencion")