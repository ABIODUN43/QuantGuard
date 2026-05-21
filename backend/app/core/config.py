from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QG_", env_file=".env", extra="ignore")

    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./quantguard_dev.db"
    secret_key: str = "dev-secret-change-me"
    environment: str = "development"
    enforce_https: bool = False
    rate_limit_per_minute: int = 120
    max_upload_bytes: int = 5 * 1024 * 1024
    access_token_expire_minutes: int = 60 * 24
    report_storage_dir: str = "generated_reports"
    cors_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5195",
        "http://localhost:5173",
    ]

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value


settings = Settings()
