from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from db.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"Tag(id: {self.id}, name: {self.name})"
