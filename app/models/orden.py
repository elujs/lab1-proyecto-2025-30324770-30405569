from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import uuid

class Orden(Base):
    __tablename__ = "ordenes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    episodio_id = Column(String, ForeignKey("episodios.id"), nullable=False)
    tipo = Column(String, nullable=False) # lab, imagen, procedimiento
    prioridad = Column(String, default="normal") # normal, urgente
    estado = Column(String, default="emitida") # emitida, autorizada, enCurso, completada, anulada
    
 
    # Contiene lista de {codigo, descripcion, indicaciones}
    detalle = Column(JSON, nullable=False) 
    fecha_emision = Column(DateTime(timezone=True), server_default=func.now())

class Prescripcion(Base):
    __tablename__ = "prescripciones"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    episodio_id = Column(String, ForeignKey("episodios.id"), nullable=False)
    
    # Items: {medicamentoCodigo, nombre, dosis, via, frecuencia, duracion}
    items = Column(JSON, nullable=False)
    observaciones = Column(Text)
    fecha_prescripcion = Column(DateTime(timezone=True), server_default=func.now())

class Resultado(Base):
    __tablename__ = "resultados"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    orden_id = Column(String, ForeignKey("ordenes.id"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    resumen = Column(Text, nullable=False)
    archivo_id = Column(String)
    version = Column(Integer, default=1)