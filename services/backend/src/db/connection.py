from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

async_engine = create_async_engine(
    settings.DATABASE_URI, future=True, echo=True
)
async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)
