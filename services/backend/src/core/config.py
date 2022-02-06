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
    # ON_DEVELOPMENT: int = int(os.getenv("DEVELOPMENT"))
    SECRET_KEY: str = secrets.token_urlsafe(32)
    AUTH_ALGORITHM: Optional[str] = os.getenv("AUTH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DB_SERVER: Optional[str] = os.getenv("DB_HOST")
    DB_USER: Optional[str] = os.getenv("DB_USERNAME")
    DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")
    DB_NAME: Optional[str] = os.getenv("DB_BASENAME")
    DATABASE_URI: Optional[PostgresDsn] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v

        db_prefix = "test_" if values.get("TESTING") else ""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            host=values.get("DB_SERVER"),
            password=values.get("DB_PASSWORD"),
            path=f"/{db_prefix}{values.get('DB_NAME') or ''}",
        )


settings = Settings()
