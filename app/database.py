from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 1. Crear el motor de la base de datos (Engine)
# Usamos la URL que leímos del archivo .env
engine = create_engine(settings.database_url)

# 2. Crear la clase SessionLocal
# Cada vez que necesitemos hablar con la BD, crearemos una instancia de esta clase
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Crear la clase Base
# Todos nuestros modelos (tablas) heredarán de esta clase
Base = declarative_base()

# 4. Dependencia para obtener la DB en los endpoints
# Esta función se usará en cada ruta para abrir y cerrar la conexión automáticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()