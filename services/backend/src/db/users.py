from datetime import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from src.db.base import Base


class User(Base):

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=dt.utcnow())
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow(), onupdate=dt.utcnow())
    bio = Column(String(300), nullable=True)
    image = Column(String(120), nullable=True)
    token = Column(String, unique=True)

    articles = relationship("Article", cascade="all,delete-orphan", backref="authors")
    comments = relationship("Comment", cascade="all,delete-orphan", backref="authors")
    favorites = relationship("Favorite", cascade="all,delete-orphan", backref="users")

    def __repr__(self) -> str:
        return f"User(username: {self.username}, email: {self.email})"


class Follow(Base):

    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    author = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))

    followers = relationship(
        "User",
        foreign_keys=[user],
        backref=backref("follower_user", cascade="all,delete-orphan"),
    )
    followings = relationship(
        "User",
        foreign_keys=[author],
        backref=backref("follower_user", cascade="all,delete-orphan"),
    )

    def __repr__(self) -> str:
        return f"Follow(user: {self.user}, author: {self.author})"
