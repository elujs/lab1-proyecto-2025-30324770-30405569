from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.schemas.auth_schema import TokenData

# Instancia para manejar la extracción del token del header
# "token" es un placeholder para la documentación del Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") 

# Credenciales y configuración del archivo .env
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Función para generar el token JWT
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_data(token: str = Depends(oauth2_scheme)):
    # Función de dependencia para DECODIFICAR y VALIDAR el token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token (verifica la firma y la expiración)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extrae los datos del payload
        username: str = payload.get("sub")
        rol: str = payload.get("rol")
        
        if username is None or rol is None:
            raise credentials_exception
        
        # Retornamos los datos para que el Router los use en el RBAC
        return TokenData(username=username, rol=rol)
        
    except JWTError:
        raise credentials_exception