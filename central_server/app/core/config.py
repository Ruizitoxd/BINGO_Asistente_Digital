from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BINGO_", env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "BINGO Central Server"
    environment: Literal["development", "testing", "production"] = "development"
    api_v1_prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"
    database_path: str = "./data/bingo.db"
    enrollment_secret: str = "CHANGE_ME_BEFORE_USE"
    token_pepper: str = "CHANGE_ME_TOKEN_PEPPER"

@lru_cache
def get_settings() -> Settings:
    return Settings()
