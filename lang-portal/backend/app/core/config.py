from pydantic_settings import BaseSettings
from pydantic import ConfigDict  # Import ConfigDict

class Settings(BaseSettings):
    # Database settings
    ENVIRONMENT: str
    
    # CORS settings
    FRONTEND_URL: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()
