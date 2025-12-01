from sqlalchemy import Column, String, DateTime
from app.database import Base
from sqlalchemy.sql import func
import uuid

class UnidadAtencion(Base):
    __tablename__ = "unidades_atencion"

    # id y datos de identificación (RF 2.1)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)
    
    # Tipo de unidad (Sede, Consultorio, Servicio)
    tipo = Column(String, nullable=False) 
    
    # Datos de contacto (RF 2.1)
    direccion = Column(String)
    telefono = Column(String)
    horario_referencia = Column(String)
    
    # Estado y Trazabilidad
    estado = Column(String, default="activo") # activo/inactivo
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())