from typing import AsyncGenerator, Tuple

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from starlette.requests import Request

async_engine = create_async_engine(
    settings.DATABASE_URI, future=True, echo=True
)
async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)
