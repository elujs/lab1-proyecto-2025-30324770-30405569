# app/routers/usuario_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from passlib.context import CryptContext
# Importamos seguridad
from app.dependencies import requires_admin

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. POST /usuarios (Protegido: Solo Admin crea usuarios)
@router.post(
    "/usuarios", 
    response_model=UsuarioResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requires_admin)] # <-- SEGURIDAD APLICADA
)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(
        (Usuario.username == usuario.username) | (Usuario.email == usuario.email)
    ).first()
    
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Username o Email ya registrados")

    hashed_password = pwd_context.hash(usuario.password)

    nuevo_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        password_hash=hashed_password,
        rol=usuario.rol
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario