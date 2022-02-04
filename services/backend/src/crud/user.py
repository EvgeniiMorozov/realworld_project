from typing import Optional

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_401_UNAUTHORIZED

from src.db.connection import get_db
from src.db.models import Follow as db_Follow, User as db_User
from src.core import auth, security
from src.schemas import user as user_schema


async def get_current_user_by_token(db: AsyncSession, token: str) -> db_User:
    """Getting a User model from a token and checking that the user exists"""
    user_db = await get_user_by_token(db, token)
    if not user_db:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="User not authorized"
        )
    return user_db


async def get_user_by_token(db: AsyncSession, token: str) -> db_User:
    """Get User model by token"""
    query = await db.execute(select(db_User).filter(db_User.token == token))
    return query.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> db_User:
    """Get user by id"""
    user_db = await db.execute(select(db_User).filter(db_User.id == user_id))
    return user_db.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> db_User:
    """Get user by username"""
    user = await db.execute(select(db_User).filter(db_User.username == username))
    return user.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> db_User:
    """Get user by email"""
    user = await db.execute(select(db_User).filter(db_User.email == email))
    return user.scalars().first()


async def create_user(db: AsyncSession, payload: user_schema.NewUserRequest) -> db_User:
    """Create and return a created user"""
    new_user = db_User(
        username=payload.user.username,
        email=payload.user.email,
        password_hash=security.get_password_hash(payload.user.password),
        token=auth.encode_jwt(payload.user.email, payload.user.password),
    )
    db.add(new_user)
    await db.commit()
    return new_user
