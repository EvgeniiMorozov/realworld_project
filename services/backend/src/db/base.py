from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin, Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta, declared_attr
from sqlalchemy.sql.sqltypes import DateTime


# class Base(metaclass=DeclarativeMeta):
#     __abstract__ = True

Base = declarative_base()


@declarative_mixin
class TimestampMixin:
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    # updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    @declared_attr
    def created_at(cls) -> Column[DateTime]:
        return Column(TIMESTAMP(timezone=True),nullable=False,  server_default=func.now())

    @declared_attr
    def updated_at(cls) -> Column[DateTime]:
        return Column(TIMESTAMP(timezone=True),nullable=False,  server_default=func.now())
