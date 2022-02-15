from base import Base, TimestampMixin
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import Table


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)
    bio = Column(String(300), nullable=True)
    image = Column(String(120), nullable=True)
    token = Column(String, unique=True)
    articles = relationship(
        "Article",
        cascade="all,delete-orphan",
        backref="authors",
    )
    comments = relationship(
        "Comment",
        cascade="all,delete-orphan",
        backref="authors",
    )
    favorites = relationship(
        "Favorite",
        cascade="all,delete-orphan",
        backref="users",
    )

    def __repr__(self) -> str:
        return f"User - username: {self.username}, email: {self.email}"


class Follow(Base):
    __tablename__ = "followers"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
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


article_tag_table = Table(
    "user_article",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE")),
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE")),
)


user_article_table = Table(
    "user_article",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE")),
)


class Article(TimestampMixin, Base):
    __tablename__ = "articles"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300))
    body = Column(Text)
    author = Column(String(80))
    tag = relationship("Tag", secondary="article_tag", backref="articles")
    favorite = relationship(
        "Favorite",
        cascade="all,delete-orphan",
        backref="articles",
    )
    comments = relationship(
        "Comment",
        cascade="all,delete-orphan",
        backref="articles",
    )

    def __repr__(self) -> str:
        return f"Article - slug: '{self.slug}', title: '{self.title}'"


class Favorite(Base):
    __tablename__ = "favorites"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Favorite - article: '{self.article}', user: {self.user}"


class Tag(Base):
    __tablename__ = "tags"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"Tag - id: {self.id}, name: '{self.name}'"


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(Text)
    author = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Comment - article: '{self.article}', author: {self.author}"
