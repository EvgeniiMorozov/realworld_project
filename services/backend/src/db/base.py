from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin, registry
from sqlalchemy.orm.decl_api import DeclarativeMeta, declared_attr
from sqlalchemy.sql.sqltypes import DateTime


mapper_registry = registry()

class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata
    __init__ = mapper_registry.constructor


# Base = declarative_base()


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
