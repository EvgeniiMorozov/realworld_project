from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError


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
