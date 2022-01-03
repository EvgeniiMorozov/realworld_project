from typing import List, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, Mapped, relationship

from base import Base, TimestampMixin

if TYPE_CHECKING:
    from .article import Article, Comment, Favorite


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=True)
    bio = Column(String(300), nullable=True)
    image = Column(String(120), nullable=True)
    token = Column(String, unique=True)
    articles: Mapped[Article] = relationship("Article", cascade="all,delete-orphan", backref="authors")
    comments: Mapped[Comment] = relationship("Comment", cascade="all,delete-orphan", backref="authors")
    favorites: Mapped[Favorite] = relationship("Favorite", cascade="all,delete-orphan", backref="users")

    def __repr__(self) -> str:
        return f"User - username: {self.username}, email: {self.email}"


class Follow(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    author = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    followers = relationship(
        "User",
        foreign_keys=[user],
        backref=backref(
            "follower_user",
            cascade="all,delete-orphan",
        ),
    )
    followings = relationship(
        "User",
        foreign_keys=[author],
        backref=backref(
            "following_user",
            cascade="all,delete-orphan",
        ),
    )

    def __repr__(self) -> str:
        return f"Follow - user: {self.user}, author: {self.user}"