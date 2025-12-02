#En Clinico ira notas clinicas, diagnostico y consentimiento

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import uuid

class NotaClinica(Base):
    __tablename__ = "notas_clinicas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    episodio_id = Column(String, ForeignKey("episodios.id"), nullable=False)
    profesional_id = Column(String, ForeignKey("profesionales.id"), nullable=False)
    
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    
    subjetivo = Column(Text, nullable=False)
    objetivo = Column(Text, nullable=False)
    analisis = Column(Text, nullable=False)
    plan = Column(Text, nullable=False)

    version = Column(String, default="1")
    es_actual = Column(Boolean, default=True)

    # Aqui esta la relacion entre notas y episodios
    episodio = relationship("EpisodioAtencion", backref="notas")
    profesional = relationship("Profesional")

class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    episodio_id = Column(String, ForeignKey("episodios.id"), nullable=False)
    
    codigo = Column(String, nullable=False) 
    descripcion = Column(String, nullable=False) 
    
    tipo = Column(String, nullable=False) # presuntivo/definitivo
    principal = Column(Boolean, default=False)

    # Aqui esta la relacion entre diagnosticos y episodios
    episodio = relationship("EpisodioAtencion", backref="diagnosticos")

class Consentimiento(Base):
    __tablename__ = "consentimientos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Vinculación (RF 2.3)
    persona_id = Column(String, ForeignKey("personas_atendidas.id"), nullable=False)
    episodio_id = Column(String, ForeignKey("episodios.id"), nullable=False)
    
    # Datos del consentimiento
    tipo_procedimiento = Column(String, nullable=False) # Ej: "Cirugía menor"
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    metodo = Column(String, nullable=False) # digital/verbal
    archivo_id = Column(String, nullable=True) # Referencia a un archivo (opcional)

    # Relaciones
    persona = relationship("PersonaAtendida")
    episodio = relationship("EpisodioAtencion", backref="consentimientos")