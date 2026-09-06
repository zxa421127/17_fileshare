from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PM Knowledge Portal"
    app_version: str = "1.1"

    database_url: str = "sqlite:///./pm_knowledge.db"

    jwt_secret_key: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "pm_minio"
    minio_secret_key: str = "pm_minio_change_me"
    minio_secure: bool = False
    minio_bucket: str = "pm-knowledge"
    download_url_expire_seconds: int = 300
    max_upload_bytes: int = 104857600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
