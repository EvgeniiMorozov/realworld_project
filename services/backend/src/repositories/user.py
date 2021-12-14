import datetime
from typing import Optional

from pydantic import SecretStr

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
        # self.db_session.add(new_user)
        result = await self.db_session.execute(new_user)
        await self.db_session.flush()

    async def get(self):
        pass

    async def get_by_email(self):
        pass

    async def get_by_username(self):
        pass

    async def update(self):
        pass

    async def authenticate(self):
        pass
