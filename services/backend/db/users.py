from datetime import datetime as dt

from sqlalchemy import Table, Column, Integer, String, DateTime

from db.base import metadata


user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False),
    Column("username", String, unique=True, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String),
    Column("created_at", DateTime, nullable=False, default=dt.utcnow()),
    Column("updated_at", DateTime, nullable=False, onupdate=dt.utcnow()),
    Column("bio", String, nullable=True),
    Column("image", String, nullable=True),
    Column("bio", String),
)
