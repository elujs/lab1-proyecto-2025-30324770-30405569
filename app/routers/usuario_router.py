from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from passlib.context import CryptContext

router = APIRouter()

# Configuración para hashear contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Buscar si el usuario o email ya existen
    usuario_existente = db.query(Usuario).filter(
        (Usuario.username == usuario.username) | (Usuario.email == usuario.email)
    ).first()
    
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Username o Email ya registrados")

    # 2. Encriptar la contraseña
    hashed_password = pwd_context.hash(usuario.password)

    # 3. Crear la instancia del modelo SQLAlchemy
    nuevo_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        password_hash=hashed_password,
        rol=usuario.rol
    )

    # 4. Guardar en BD
    db.add(nuevo_usuario)
    db.commit()      # Confirmar transacción
    db.refresh(nuevo_usuario) # Recargar el objeto con los datos generados por la BD (id, fecha)

    return nuevo_usuario