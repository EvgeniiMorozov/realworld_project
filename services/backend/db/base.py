from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from core.config import DATABASE_URL


database = Database(DATABASE_URL)
metadata = MetaData()
# engine = create_engine(DATABASE_URL, echo=True)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
