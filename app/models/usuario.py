from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    estado = Column(String, default="activo") 
    # Roles permitidos: administracion, profesional, cajero, auditor
    rol = Column(String, default="profesional") 
        # func.now() para que en la base de datos ponga la hora exacta automáticamente
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())