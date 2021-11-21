from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import get_session
from db.users import User, Follow
from starlette.status import HTTP_401_UNAUTHORIZED


class UserRepository:
    def create_user(self):
        pass

    def change_user(self):
        pass

    def get_current_user_by_token(self):
        pass

    def get_user_by_token(self):
        pass

    def get_user_by_username(self):
        pass

    def get_user_by_email(self):
        pass

    def create_subscribe(self):
        pass

    def delete_subscribe(self):
        pass

    def check_subscribe(self, db: AsyncSession, follower: str, following: str) -> bool:
        check = db.query(Follow).filter(Follow.user == follower, Follow.author == following)
        return db.query(check.exists()).scalar()
