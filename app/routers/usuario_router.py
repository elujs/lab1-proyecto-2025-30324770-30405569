from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.dependencies import requires_admin
from app.services import usuario_service

router = APIRouter()

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_admin)])
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.create_usuario(db, usuario)