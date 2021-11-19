from datetime import datetime as dt

from sqlalchemy import Column, String, Integer, DateTime

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=dt.utcnow())
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow(), onupdate=dt.utcnow())
    bio = Column(String(300), nullable=True)
    image = Column(String(120), nullable=True)
