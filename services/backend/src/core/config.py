import os
import pathlib
import secrets
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, validator
from pydantic.networks import PostgresDsn

current_path = pathlib.Path.cwd().absolute()
dotenv_path = current_path.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):

    TESTING: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    AUTH_ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POSTGRES_HOST: Optional[str] = os.getenv("DB_HOST")
    DB_PORT: Optional[str] = os.getenv("DB_PORT")
    POSTGRES_USER: Optional[str] = os.getenv("DB_USERNAME")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")
    POSTGRES_DB: Optional[str] = os.getenv("DB_NAME")
    DATABASE_URI: Optional[PostgresDsn] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v

        db_prefix = "test_" if values.get("TESTING") else ""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=int(values.get("DB_PORT")) or 5432,
            path=f"/{db_prefix}{values.get('POSTGRES_DB') or ''}",
        )

    @property
    def alembic_database_url(self) -> Optional[str]:
        return (
            self.DATABASE_URI.replace(
                "postgresql+asyncpg://", "postgresql+psycopg2://"
            )
            if self.DATABASE_URI
            else self.DATABASE_URI
        )


settings = Settings()
