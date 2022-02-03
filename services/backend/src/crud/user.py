from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_401_UNAUTHORIZED

from src.db.connection import get_db
from src.db.models import Follow as db_Follow, User as db_User
from src.core import auth
from src.schemas import user, profile


async def get_current_user_by_token(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(auth.check_token),
) -> db_User:
    """Getting a User model from a token and checking that the user exists."""
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="User not authorized"
        )
    return user


async def get_user_by_token(db: AsyncSession, token: str) -> db_User:
    """Get User model by token"""
    user = await db.execute(select(db_User).filter(db_User.token == token))
    return user.scalars().first()
