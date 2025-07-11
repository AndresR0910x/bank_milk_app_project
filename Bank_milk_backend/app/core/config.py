import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

# Validación manual opcional
if not settings.DATABASE_URL or not settings.SECRET_KEY:
    raise ValueError("❌ Faltan variables obligatorias en el archivo .env")
