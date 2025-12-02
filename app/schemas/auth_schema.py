from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    # Respuesta que devuelve el servidor al hacer login
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None 

class TokenData(BaseModel):
    # Payload que se guarda dentro del token JWT
    username: Optional[str] = None
    rol: Optional[str] = None

class LoginRequest(BaseModel):
    # Pydantic schema para recibir credenciales en el POST /auth/login
    username: str
    password: str