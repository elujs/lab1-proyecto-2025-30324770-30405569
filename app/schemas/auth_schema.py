from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None 

class TokenData(BaseModel):
    
    username: Optional[str] = None
    rol: Optional[str] = None

class LoginRequest(BaseModel):
    
    username: str
    password: str