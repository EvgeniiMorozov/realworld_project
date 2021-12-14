import asyncio
import datetime
from typing import Optional

from pydantic import SecretStr, EmailStr
from sqlalchemy.sql.expression import select

import src.db as db
import src.schemas as schemas
from base import BaseRepository
from src.core.security import get_password_hash


class UserRepository(BaseRepository):
    async def create(self, payload: schemas.UserCreate) -> Optional[int]:
        new_user = db.User(
            username=payload.username,
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get(self, user_id: int) -> Optional[schemas.UserDB]:
        query = select(db.User).where(db.User.c.id == user_id)
        result = await self.db_session.execute(query)
        await self.db_session.flush()
        return schemas.UserDB(**result.scalars().first()) if result else None

    async def get_by_email(self, user_email: EmailStr) -> Optional[schemas.UserDB]:
        query = select(db.User).where(db.User.c.email == user_email)
        result = await self.db_session.execute(query)
        await self.db_session.flush()
        return

    async def get_by_username(self):
        pass

    async def update(self):
        pass

    async def authenticate(self):
        pass
