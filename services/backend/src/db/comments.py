from datetime import datetime as dt

from db.base import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text


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
