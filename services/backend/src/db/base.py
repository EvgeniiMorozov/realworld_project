from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.orm import declarative_base, declarative_mixin
from sqlalchemy.orm.decl_api import DeclarativeMeta

class Base(metaclass=DeclarativeMeta):
    __abstract__ = True


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
