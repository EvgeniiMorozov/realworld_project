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
    """Getting a User model from a token and checking that the user exists"""
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


async def get_user_by_username(db: AsyncSession, username: str) -> db_User:
    """Get User model by username"""
    user = await db.execute(select(db_User).filter(db_User.username == username))
    return user.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> db_User:
    """Get User model by email"""
    user = await db.execute(select(db_User).filter(db_User.email == email))
    return user.scalars().first()


async def create_user(db: AsyncSession, new_user: user.UserCreate) -> db_User:
    """Create and return a created User model"""
    db_user = db_User(
        token=auth.encode_jwt(new_user.email, new_user.password),
        username=new_user.user.username,
        email=new_user.email,
        )
    db.add(db_user)
    await db.commit()
    return db_user
