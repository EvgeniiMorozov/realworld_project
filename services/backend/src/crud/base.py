from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session


class CRUDBase:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session
