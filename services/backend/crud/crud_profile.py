from typing import Optional

import db
import models
from crud import crud_user
from db.base import database


async def get_profile_by_username(
    username: str, requested_user: Optional[models.UserDB] = None
) -> Optional[models.Profile]:
    user_db = await crud_user.get_user_by_username(username=username)
    if user_db is None:
        return None
    profile = models.Profile(username=user_db.username, bio=user_db.bio, image=user_db.image)
    profile.following = await is_following(user_db, requested_user)
    return profile


async def get_profile_by_user_id(
    user_id: int, requested_user: Optional[models.UserDB] = None
) -> Optional[models.Profile]:
    user_db = await crud_user.get(user_id=user_id)
    if user_db is None:
        return None
    profile = models.Profile(username=user_db.username, bio=user_db.bio, image=user_db.image)
    profile.following = await is_following(user_db, requested_user)
    return profile


async def is_following(follower: models.UserDB, follower_by: Optional[models.UserDB]) -> bool:
    if follower_by is None:
        return False
    query = (
        db.followers_assoc.select()
        .where(follower.id == db.followers_assoc.c.follower)
        .where(follower_by.id == db.followers_assoc.c.followed_by)
    )
    row = await database.fetch_one(query=query)
    return row is not None