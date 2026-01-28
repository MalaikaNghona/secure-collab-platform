'EOF'
"""
Application configuration with security-focused defaults.

Security Design Decisions:
1. Secrets loaded from environment, never hardcoded
2. Validation fails fast if required secrets are missing
3. Sensible secure defaults where possible
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Pydantic automatically loads from .env file and environment.
    Environment variables take precedence over .env file.
    """
    
    # JWT Settings
    secret_key: str = Field(
        ...,  # Required - app won't start without it
        description="Secret key for JWT signing"
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        le=1440,
        description="Token expiration time in minutes"
    )
    
    # Database
    database_url: str = Field(
        default="sqlite:///./secure_collab.db",
        description="Database connection string"
    )
    
    # Environment
    environment: str = Field(
        default="development",
        description="Current environment"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).
    
    Using lru_cache means settings are loaded once at startup.
    """
    return Settings()
