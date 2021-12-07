from typing import Any

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import as_declarative

from src.core.config import DATABASE_URL


async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


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
