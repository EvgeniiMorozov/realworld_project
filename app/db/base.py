from databases import Database
from sqlalchemy import MetaData, create_engine

from core.config import settings

print(f"******* {settings.async_database_url}")
database = Database(settings.async_database_url)
metadata = MetaData()
engine = create_engine(settings.async_database_url, echo=True)
