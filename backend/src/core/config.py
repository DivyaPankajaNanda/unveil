from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    PROJECT_NAME = "Unveil"
    API_V1 : str = "/api/v1"
    JWT_SECRET_KEY : str = config("JWT_SECRET_KEY", cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60*24*2
    

    MONGODB_CONNECTION_STRING = config("MONGODB_CONNECTION_STRING", cast=str)
    
    class Config:
        case_sensitive = True

settings = Settings()