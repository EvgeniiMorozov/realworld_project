from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.orm import declarative_base, declarative_mixin

Base = declarative_base()


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
