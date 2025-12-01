# app/models/persona.py

from sqlalchemy import Column, String, DateTime, Date
from app.database import Base
import uuid
from sqlalchemy.sql import func

class PersonaAtendida(Base):
    __tablename__ = "personas_atendidas"

    # Datos Mínimos del Requerimiento 2.1
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo_documento = Column(String, nullable=False)
    numero_documento = Column(String, unique=True, index=True, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(String, nullable=False)
    
    # Datos de Contacto
    correo = Column(String, index=True)
    telefono = Column(String)
    direccion = Column(String)
    contacto_emergencia = Column(String)
    
    # Opcionales (Requisito 2.1)
    alergias = Column(String)
    antecedentes_resumen = Column(String)
    
    # Estado
    estado = Column(String, default="activo") # activo/inactivo
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())