from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str
    
    # AI Config
    ai_model: str = "gemini-3-flash-preview"
    price_input: float = 0.50
    price_output: float = 3.0
    
    # App config
    debug: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

@lru_cache
def get_settings():
    return Settings()