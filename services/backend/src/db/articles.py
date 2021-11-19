from datetime import datetime as dt

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    slug = Column(String(100), unique=True)
    title = Column(String(100))
    description = Column(Text)
    body = Column(Text)
    author = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    created_at = Column(DateTime, default=dt.utcnow())
    updated_at = Column(DateTime, default=dt.utcnow(), onupdate=dt.utcnow())

    def __repr__(self) -> str:
        return f"Article(slug: {self.slug}, title: {self.title})"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"Tag(id: {self.id}, name: {self.name})"


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Favorite(article: {self.article}, user: {self.user})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(Text)
    author = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))
    created_at = Column(DateTime, nullable=False, default=dt.utcnow())
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow(), onupdate=dt.utcnow())

    def __repr__(self) -> str:
        return f"Comment(article: {self.article}, author: {self.author})"
