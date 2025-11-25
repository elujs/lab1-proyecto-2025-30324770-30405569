from fastapi import FastAPI
from app.database import engine, Base
# Importamos el modelo para que SQLAlchemy cree la tabla al inicio
from app.models import usuario 
# Importamos el router para exponer los endpoints HTTP
from app.routers import usuario_router

# Crea las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Médica",
    version="0.1.0"
)

# Registramos las rutas de usuario en la aplicación principal
app.include_router(usuario_router.router, tags=["Usuarios"])
# --------------------------

@app.get("/")
def read_root():
    return {"mensaje": "¡La API está viva, funcionando y conectada a la BD!"}