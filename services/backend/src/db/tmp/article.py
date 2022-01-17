from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from base import Base, TimestampMixin

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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slug = Column(String(100), unique=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300))
    body = Column(Text)
    author = Column(String(80))
    tag = relationship("Tag", secondary="article_tag", backref="articles")
    favorite = relationship("Favorite", cascade="all,delete-orphan", backref="articles")
    comments = relationship("Comment", cascade="all,delete-orphan", backref="articles")

    def __repr__(self) -> str:
        return f"Article - slug: '{self.slug}', title: '{self.title}'"


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(String(80), ForeignKey("users.username", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Favorite - article: '{self.article}', user: {self.user}"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"Tag - id: {self.id}, name: '{self.name}'"


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body = Column(Text)
    author = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    article = Column(String(100), ForeignKey("articles.slug", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Comment - article: '{self.article}', author: {self.author}"

