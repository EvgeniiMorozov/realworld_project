import secrets
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    TESTING: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "root"
    POSTGRES_PASSWORD: str = "Zz123456"
    POSTGRES_DB: str = "realworld_project"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        db_prefix = "test_" if values.get("TESTING") else ""
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            # port="5432",
            path=f"/{db_prefix}{values.get('POSTGRES_DB') or ''}"
        )


settings = Settings()
