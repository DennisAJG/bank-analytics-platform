from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BANK_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "bank-analytics-api"
    environment: str = "dev"
    log_level: str = "INFO"

    host: str = "0.0.0.0"
    port: int = 8001

    database_url: str = "postgresql+psycopg://bankuser:bankpass@localhost:5433/bankdb"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30


settings = Settings()
