from sqlalchemy.ext.asyncio import AsyncSession

from db.users import User
from repositories.users import UserRepository


def add_following(db: AsyncSession, user: User, follower: User) -> User:
    subscribe = UserRepository.check_subscribe(db, follower.username, user.username)
    if subscribe:
        user.following = True
    return user
