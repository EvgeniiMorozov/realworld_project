from typing import Any

from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, declarative_mixin


from src.core.config import settings


async_engine = create_async_engine(settings.DATABASE_URI, echo=True, future=True)


@as_declarative()
class Base(object):
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
