from datetime import datetime as dt

from sqlalchemy import Table, Column, Integer, String, DateTime

from db.base import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, index=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("bio", String, index=True),
    Column("image", String, nullable=True),
    Column("hashed_password", String, nullable=False),
)
