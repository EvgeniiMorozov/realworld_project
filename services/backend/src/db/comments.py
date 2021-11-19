from datetime import datetime as dt

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text

from db.base import Base


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