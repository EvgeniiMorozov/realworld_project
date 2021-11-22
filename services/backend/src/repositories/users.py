from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import get_session
from db.users import User, Follow
from starlette.status import HTTP_401_UNAUTHORIZED

from models.users import NewUserRequest, UserResponce
from core import auth


class UserRepository:
    def create_user(self, db: AsyncSession, user: NewUserRequest):
        """Create and return a created User model."""
        db_user = User(
            token=auth.encode_jwt(user.user.email, user.user.password),
            username=user.user.username,
            email=user.user.email,
            password=user.user.password,
            bio="default",
            image="default",
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def change_user(
        self, db: AsyncSession, user: UserResponce, data: UserResponce
    ) -> User:
        """Update and return User model."""
        upd_user = (
            update(User)
            .where(User.token == user.user.token)
            .values(**data.user.dict(exclude_unset=True))
        )
        # upd_user = update(User).where(User.token == user.token).values(**data.user.dict(exclude_unset=True))
        db.execute(upd_user)
        db.commit()
        return db.query(User).filter(User.token == user.user.token).first()

    def get_current_user_by_token(
        self,
        db: AsyncSession = Depends(get_session),
        token: str = Depends(auth.check_token),
    ) -> User:
        """Getting a User model from a token and checking that the user exists."""
        user = self.get_user_by_token(db, token)
        if not user:
            raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Not authorized")
        return self.get_user_by_token(db, token)

    def get_user_by_token(self, db: AsyncSession, token: str) -> User:
        """Get User model by token."""
        return db.query(User).filter(User.token == token).first()

    def get_user_by_username(self, db: AsyncSession, username: str) -> User:
        """Get User model by username."""
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: AsyncSession, email: EmailStr) -> User:
        """Get User model by email."""
        return db.query(User).filter(User.email == email).first()

    def create_subscribe(
        self, db: AsyncSession, user_username: str, author_username: str
    ) -> None:
        """Create Follow model by user and author username."""
        db_subscribe = Follow(user=user_username, author=author_username)
        db.add(db_subscribe)
        db.commit()

    def delete_subscribe(
        self, db: AsyncSession, user_username: str, author_username: str
    ) -> None:
        """Delete Follow model by user and author username."""
        subscribe = delete(Follow).where(
            Follow.user == user_username, Follow.author == author_username
        )
        db.execute(subscribe)
        db.commit()

    def check_subscribe(self, db: AsyncSession, follower: str, following: str) -> bool:
        check = db.query(Follow).filter(
            Follow.user == follower, Follow.author == following
        )
        return db.query(check.exists()).scalar()
