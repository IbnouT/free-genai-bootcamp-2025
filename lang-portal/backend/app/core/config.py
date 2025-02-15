from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    ENVIRONMENT: str
    
    # CORS settings
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

settings = Settings() 