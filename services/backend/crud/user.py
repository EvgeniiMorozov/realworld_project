from typing import Optional

from pydantic import SecretStr

import db
from db.base import database
import models
from core.security import get_password_hash, verify_password


async def create(payload: models.UserCreate) -> Optional[int]:
    query = db.users.insert().values(
        username=payload.username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
    )
    return database.execute(query=query)


async def get(user_id: int) -> Optional[models.UserDB]:
    query = db.users.select().where(user_id == db.users.c.id)
    user_row = await database.fetch_one(query=query)
    return models.UserDB(**user_row) if user_row else None
