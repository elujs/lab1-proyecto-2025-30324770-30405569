# app/main.py

from fastapi import FastAPI
from app.database import engine, Base
# Importamos los modelos para que SQLAlchemy cree las tablas al inicio
from app.models import usuario 
from app.models import persona 
from app.models import profesional
from app.models import unidad

# Importamos los routers para exponer los endpoints HTTP
from app.routers import usuario_router
from app.routers import persona_router
from app.routers import profesional_router
from app.routers import unidad_router 
# Crea las tablas en la BD si no existen
# Esto creará la nueva tabla 'unidades_atencion'
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Médica",
    version="0.1.0"
)

# Registramos las rutas
app.include_router(usuario_router.router, tags=["Usuarios", "Seguridad"])
app.include_router(persona_router.router, tags=["PersonasAtendidas", "Identidades"])
app.include_router(profesional_router.router, tags=["Profesionales", "Identidades"])
app.include_router(unidad_router.router, tags=["UnidadesAtencion", "Identidades"]) 

@app.get("/")
def read_root():
    return {"mensaje": "¡La API está viva, funcionando y conectada a la BD!"}