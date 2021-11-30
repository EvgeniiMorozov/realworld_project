from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from src.core import auth
from src.crud.base import CRUDBase
from src.crud.users import get_user_by_token
from src.db.base import get_session
from src.db.users import Follow
from src.db.users import User
from src.models.users import NewUserRequest, UpdateUserRequest, UserResponce, User as UserDB


class UserRepository(CRUDBase):
    async def create_user(self, user: NewUserRequest) -> UserDB:
        db_user = User(
            token=auth.encode_jwt(user.user.email, user.user.password),
            username=user.user.username,
            email=user.user.email,
            password=user.user.password,
            bio="default",
            image="default",
        )
        await self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def change_user(self, user: UserResponce, data: UpdateUserRequest) -> User:
        """Update and return User model."""
        upd_user = update(User).where(User.token == user.user.token).values(**data.user.dict(exclude_unset=True))
        # upd_user = update(User).where(User.token == user.token).values(**data.user.dict(exclude_unset=True))
        await self.session.execute(upd_user)
        await self.session.commit()
        return await self.session.query(User).filter(User.token == user.user.token).first()

    def get_current_user_by_token(self, token: str = Depends(auth.check_token)) -> User:
        """Getting a User model from a token and checking that the user exists."""
        user = get_user_by_token(db, token)
        if not user:
            raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Not authorized")
        return get_user_by_token(db, token)
