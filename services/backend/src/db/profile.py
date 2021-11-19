from sqlalchemy import Column, ForeignKey, Integer

from db.base import Base
from db.database import reference_column





class UserProfile(Base):
    __tablename__ = "userprofile"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = reference_column("users", nullable=False)
