from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth_schema import LoginRequest, Token
from app.services.auth_service import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Seguridad"])

# Configuración para hashear contraseñas (la misma que en usuario_router)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=Token)
def login_for_access_token(request: LoginRequest, db: Session = Depends(get_db)):
    # 1. Buscar usuario
    user = db.query(Usuario).filter(Usuario.username == request.username).first()
    
    if not user:
        # Usamos el mismo mensaje de error para evitar ataques de enumeración de usuarios
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        
    # 2. Verificar la contraseña hasheada
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    # 3. Generar el JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Payload: 'sub' (subject) y 'rol'
    access_token = create_access_token(
        data={"sub": user.username, "rol": user.rol},
        expires_delta=access_token_expires
    )
    
    # 4. Devolver el token
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }