from datetime import datetime as dt

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Table
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


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Favorite(article: {self.article}, user: {self.user})"


article_tag_table = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE")),
    Column("tags_name", ForeignKey("tags.name", ondelete="CASCADE")),
)


user_article_table = Table(
    "article_tag",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE")),
)
