from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Doctor Collaboration Bot"
    
    # LLM Configuration
    OLLAMA_API_URL: str = "http://localhost:11434"
    LLM_MODEL_NAME: str = "medllama2"  # or "meditron"
    
    # Database Configuration
    JSON_DB_PATH: str = "db/data.json"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        case_sensitive = True

settings = Settings()
