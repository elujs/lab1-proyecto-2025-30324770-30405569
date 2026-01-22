from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.auth_schema import Token
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Seguridad"])

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Llamamos a la lógica del servicio
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "rol": user.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": auth_service.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }