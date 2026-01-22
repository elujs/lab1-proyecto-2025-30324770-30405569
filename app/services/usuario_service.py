from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.services.auth_service import pwd_context # Reutilizamos el contexto centralizado

def create_usuario(db: Session, usuario: UsuarioCreate):
    existing = db.query(Usuario).filter((Usuario.username == usuario.username) | (Usuario.email == usuario.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuario o email ya registrados")

    new_user = Usuario(
        username=usuario.username,
        email=usuario.email,
        password_hash=pwd_context.hash(usuario.password),
        rol=usuario.rol
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user