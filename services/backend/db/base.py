from core.config import DATABASE_URL
from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, echo=True)
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
