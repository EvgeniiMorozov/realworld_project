from core.config import settings
from databases import Database
from sqlalchemy import (
    MetaData,
    create_engine
)


# print(f"******* {settings.async_database_url}")
database = Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
