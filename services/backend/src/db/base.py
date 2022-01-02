from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin, Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta


# class Base(metaclass=DeclarativeMeta):
#     __abstract__ = True

Base = declarative_base()


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
