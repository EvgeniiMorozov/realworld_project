from databases import Database
from sqlalchemy import MetaData, create_engine

from core.config import settings

print(f"******* {settings.SQLALCHEMY_DATABASE_URI}")
database = Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
