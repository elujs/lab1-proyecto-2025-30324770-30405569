# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # <-- NUEVO IMPORT NECESARIO
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth_schema import LoginRequest, Token # Mantener LoginRequest para referencia, aunque ya no se usa directamente
from app.services.auth_service import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Seguridad"])

# Configuración para hashear contraseñas (la misma que en usuario_router)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=Token)
# CAMBIO CLAVE: Usa OAuth2PasswordRequestForm para leer los datos del formulario (Form-Data)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # 1. Buscar usuario (usamos form_data.username)
    user = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        
    # 2. Verificar la contraseña hasheada (usamos form_data.password)
    if not verify_password(form_data.password, user.password_hash):
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