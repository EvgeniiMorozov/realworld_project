import datetime
from typing import Optional

from pydantic import SecretStr
from services.backend.src.db.models import User

import src.db as db
import src.schemas as schemas
from base import BaseRepository
from src.core.security import get_password_hash


class UserRepository(BaseRepository):
    async def create(self, payload: schemas.UserCreate) -> Optional[int]:
        query = User(
            username=payload.username,
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            )
        await self._db_session(query)
        await self._db_session.commit()
        self._db_session.refresh(query)


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
