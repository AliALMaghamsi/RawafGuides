from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    API_PREFIX:str
    DEBUG:bool
    DATABASE_URL:str
    ALLOWED_ORIGINS:str
    ADMIN_USERNAME:str
    ADMIN_PASSWORD:str
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    ALGORITHM:str
    BATCH_SIZE:int
    

    @field_validator("ALLOWED_ORIGINS")
    def parsed_allowed_origins(cls, v:str):
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
