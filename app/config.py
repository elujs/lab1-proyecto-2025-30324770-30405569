from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Estas variables deben coincidir con las del archivo .env
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

# Instanciamos la configuración para usarla en cualquier parte
settings = Settings()