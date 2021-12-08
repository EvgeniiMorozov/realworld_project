from sqlalchemy import Column, String, TIMESTAMP, func

from base import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=True)
    bio = Column(String(300), nullable=True)
    image = Column(String(120), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    token = Column(String, unique=True)

