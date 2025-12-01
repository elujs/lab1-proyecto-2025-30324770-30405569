
from sqlalchemy import Column, String, Boolean, DateTime
from app.database import Base
from sqlalchemy.sql import func
import uuid

class Profesional(Base):
    __tablename__ = "profesionales"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    registro_profesional = Column(String, unique=True, nullable=False) # Clave de unicidad
    categoria = Column(String, nullable=False)
    especialidad = Column(String)
    correo = Column(String)
    telefono = Column(String)
    
    # Campo específico del requisito 2.1
    agenda_habilitada = Column(Boolean, default=True) 
    
    estado = Column(String, default="activo") # activo/inactivo
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())