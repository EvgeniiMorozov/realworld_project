from typing import AsyncGenerator, Tuple

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request


def create_engine(db_url: str) -> Tuple[AsyncEngine, AsyncSession]:
    """Create async engine for application"""
    async_engine = create_async_engine(db_url, future=True, echo=True)
    async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
    return async_engine, async_session


async def get_db(request: Request) -> AsyncGenerator:
    """Dependency function that yields db sessions"""
    db = request.app.state.sessionmaker()
    try:
        yield db
    except SQLAlchemyError as error:
        await db.rollback()
        raise error
    finally:
        await db.close()
