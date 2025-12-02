from fastapi import FastAPI
from app.database import engine, Base
# Importamos todos los modelos para crear las tablas
from app.models import usuario 
from app.models import persona 
from app.models import profesional
from app.models import unidad
from app.models import agenda
from app.models import cita
from app.models import episodio 
from app.models import clinico  #(Notas, Diagnósticos, Consentimientos)

# Importamos todos los routers
from app.routers import usuario_router
from app.routers import persona_router
from app.routers import profesional_router
from app.routers import unidad_router 
from app.routers import agenda_router
from app.routers import cita_router
from app.routers import episodio_router
from app.routers import clinico_router  
from app.routers import auth_router #router de autenticación

# Crea las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Médica",
    version="0.1.0",
    docs_url="/api_docs"
)

# Registramos las rutas
app.include_router(auth_router.router)
app.include_router(usuario_router.router, tags=["Usuarios", "Seguridad"])
app.include_router(persona_router.router, tags=["PersonasAtendidas", "Identidades"])
app.include_router(profesional_router.router, tags=["Profesionales", "Identidades"])
app.include_router(unidad_router.router, tags=["UnidadesAtencion", "Identidades"])
app.include_router(agenda_router.router, tags=["Agendas", "Citas"])
app.include_router(cita_router.router, tags=["Citas"])
app.include_router(episodio_router.router, tags=["Episodios", "Clínico"])
app.include_router(clinico_router.router, tags=["Clínico"]) 
@app.get("/")
def read_root():
    return {"mensaje": "¡La API está funcionando y conectada a la BD!"}