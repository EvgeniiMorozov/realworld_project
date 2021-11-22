from core.config import DATABASE_URL
# from databases import Database
# from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# database = Database(DATABASE_URL)
# metadata = MetaData()
# engine = create_engine(DATABASE_URL, echo=True)
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
