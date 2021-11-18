from datetime import datetime as dt

from db.base import Base


class User(Base):
    __tablename__ = "users"
    username = Column()
