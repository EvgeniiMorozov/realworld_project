from sqlalchemy import Column, String, TIMESTAMP, func, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship, backref

from base import Base, TimestampMixin


class User(Base):
    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)
    bio = Column(String(300), nullable=True)
    image = Column(String(120), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    token = Column(String, unique=True)
    articles = relationship("Article", cascade="all,delete-orphan", backref="authors")
    comments = relationship("Comment", cascade="all,delete-orphan", backref="authors")
    favorites = relationship("Favorite", cascade="all,delete-orphan", backref="users")

    def __repr__(self):
        return f"User - username: {self.username}, email: {self.email}"


class Follow(Base):
    __tablename__ = "followers"

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

    def __repr__(self):
        return f"Follow - user: {self.user}, author: {self.user}"


class ArticleTag(Base):
    __tablename__ = "article_tag"

    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    tag_name = Column(String(50), ForeignKey("tags.name", ondelete="CASCADE"))


class UserArticle(Base):
    __tablename__ = "user_article"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    article_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))


class Article(TimestampMixin, Base):
    __tablename__ = "articles"

    slug = Column(String(100), unique=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300))
    body = Column(Text)
    author = Column(String(80))
    tag = relationship("Tag", secondary="article_tag", backref="articles")
    favorite = relationship("Favorite", cascade="all,delete-orphan", backref="articles")
    comments = relationship("Comment", cascade="all,delete-orphan", backref="articles")

    def __repr__(self):
        return f"Article - slug: '{self.slug}', title: '{self.title}'"


class Favorite(Base):
    __tablename__ = "favorites"

    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self):
        return f"Favorite - article: '{self.article}', user: {self.user}"


class Tag(Base):
    __tablename__ = "tags"

    name = Column(String(50), unique=True)

    def __repr__(self):
        return f"Tag - id: {self.id}, name: '{self.name}'"


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"

    body = Column(Text)
    author = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self):
        return f"Comment - article: '{self.article}', author: {self.author}"
