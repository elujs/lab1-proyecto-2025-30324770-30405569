# app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.models import usuario 
from app.models import persona 
from app.models import profesional
from app.models import unidad
from app.models import agenda
from app.models import cita

from app.routers import usuario_router
from app.routers import persona_router
from app.routers import profesional_router
from app.routers import unidad_router 
from app.routers import agenda_router
from app.routers import cita_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Médica",
    version="0.1.0"
)


app.include_router(usuario_router.router, tags=["Usuarios", "Seguridad"])
app.include_router(persona_router.router, tags=["PersonasAtendidas", "Identidades"])
app.include_router(profesional_router.router, tags=["Profesionales", "Identidades"])
app.include_router(unidad_router.router, tags=["UnidadesAtencion", "Identidades"]) 
app.include_router(agenda_router.router, tags=["Agendas", "Identidades"])
app.include_router(cita_router.router, tags=["Citas"])

@app.get("/")
def read_root():
    return {"mensaje": "¡La API está viva, funcionando y conectada a la BD!"}