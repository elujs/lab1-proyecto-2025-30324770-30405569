from fastapi import FastAPI
from app.database import engine, Base

# IMPORTACIÓN DE MODELOS
from app.models import (
    usuario, persona, profesional, unidad, 
    agenda, cita, episodio, clinico, orden,
    cobertura, facturacion
)

#IMPORTACIÓN DE ROUTERS 
from app.routers import (
    auth_router, usuario_router, persona_router, 
    profesional_router, unidad_router, agenda_router, 
    cita_router, episodio_router, clinico_router, 
    orden_router, financiero_router
)

# CREACIÓN DE TABLAS 
# Esto crea todas las tablas en PostgreSQL si aún no existen
Base.metadata.create_all(bind=engine)

#CONFIGURACIÓN DE LA APP 
app = FastAPI(
    title="API Gestión Médica Integral",
    version="1.0.0",
    description="Sistema completo de gestión hospitalaria: Identidades, Citas, Historias Clínicas, Órdenes y Facturación.",
    docs_url="/api_docs"
)

#  REGISTRO DE RUTAS (ROUTERS) 

# Seguridad y Acceso
app.include_router(auth_router.router, tags=["Seguridad"])
app.include_router(usuario_router.router, prefix="/api/v1", tags=["Usuarios"])

# Identidades (Sección 2.1)
app.include_router(persona_router.router, prefix="/api/v1", tags=["Personas Atendidas"])
app.include_router(profesional_router.router, prefix="/api/v1", tags=["Profesionales"])
app.include_router(unidad_router.router, prefix="/api/v1", tags=["Unidades de Atención"])

# Agenda y Citas (Sección 2.2)
app.include_router(agenda_router.router, prefix="/api/v1", tags=["Agendas"])
app.include_router(cita_router.router, prefix="/api/v1", tags=["Citas y Seguimiento"])

# Registro Clínico y Órdenes (Secciones 2.3 y 2.4)
app.include_router(episodio_router.router, prefix="/api/v1", tags=["Episodios Clínicos"])
app.include_router(clinico_router.router, prefix="/api/v1", tags=["Registro Médico"])
app.include_router(orden_router.router, prefix="/api/v1", tags=["Órdenes y Prestaciones"])

# Cobertura, Catálogo y Facturación (Secciones 2.5, 2.6 y 2.7)
app.include_router(financiero_router.router, prefix="/api/v1", tags=["Financiero y Cobertura"])

# ENDPOINTS GENERALES 
@app.get("/", tags=["General"])
def read_root():
    return {
        "mensaje": "¡API Gestión Médica funcionando con éxito!",
        "documentacion": "/api_docs",
        "estado": "Conectado a PostgreSQL"
    }

@app.get("/health", tags=["Observabilidad"])
def health_check():
    return {"status": "ok", "service": "api-gestion-medica"}