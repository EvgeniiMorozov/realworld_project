from sqlalchemy import TIMESTAMP, Column, Integer, func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declarative_mixin


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True, index=True)


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
