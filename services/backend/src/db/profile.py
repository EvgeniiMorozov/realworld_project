from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from db.database import reference_column
from db.users import User


class Followers(Base):
    __tablename__ = "followers_assoc"
    follower = Column(Integer, ForeignKey("userprofile.user_id"))
    followed_by = Column(Integer, ForeignKey("userprofile.user_id"))


class UserProfile(Base):
    __tablename__ = "userprofile"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = reference_column("users", nullable=False)

