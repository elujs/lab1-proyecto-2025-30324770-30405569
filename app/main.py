from fastapi import FastAPI
from app.database import engine, Base

# routers
from app.routers import usuario_router
from app.routers import persona_router
from app.routers import profesional_router
from app.routers import unidad_router 
from app.routers import agenda_router
from app.routers import cita_router
from app.routers import episodio_router
from app.routers import clinico_router  
from app.routers import auth_router 
from app.routers import financiero_router
# Importacion de modelos
from app.models import (
    usuario, persona, profesional, unidad, 
    agenda, cita, episodio, clinico, orden 
)

# Importacion de routers
from app.routers import (
    auth_router, usuario_router, persona_router, 
    profesional_router, unidad_router, agenda_router, 
    cita_router, episodio_router, clinico_router, 
    orden_router # <-- router de órdenes agregado
)


Base.metadata.create_all(bind=engine)
print("--- ¡CONEXIÓN EXITOSA! TABLAS CREADAS ---")

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Médica",
    version="0.2.0", 
    docs_url="/api_docs"
)
print("--- INTENTANDO CONECTAR A LA BASE DE DATOS ---") 

# --- REGISTRO DE RUTAS ---
app.include_router(auth_router.router)
app.include_router(usuario_router.router, tags=["Usuarios", "Seguridad"])
app.include_router(persona_router.router, tags=["Personas Atendidas", "Identidades"])
app.include_router(profesional_router.router, tags=["Profesionales", "Identidades"])
app.include_router(unidad_router.router, tags=["Unidades de Atención", "Identidades"])
app.include_router(agenda_router.router, tags=["Agendas", "Citas"])
app.include_router(cita_router.router, tags=["Citas"])
app.include_router(episodio_router.router, tags=["Episodios", "Clínico"])
app.include_router(clinico_router.router, tags=["Clínico"]) 
@app.get("/")
def read_root():
    return {"mensaje": "¡La API está funcionando y conectada a la BD!"}

app.include_router(financiero_router.router, tags=["Financiero y Cobertura"])
app.include_router(clinico_router.router, tags=["Registro Clínico"])
app.include_router(orden_router.router, tags=["Órdenes y Prestaciones"]) 
@app.get("/", tags=["General"])
def read_root():
    return {"mensaje": "¡La API está funcionando y conectada a la BD!"}

@app.get("/health", tags=["Observabilidad"])
def health_check():
    return {"status": "ok", "service": "api-gestion-medica"}