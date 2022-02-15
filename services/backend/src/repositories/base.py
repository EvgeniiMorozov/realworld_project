from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(
        self,
        db_session: AsyncSession,
        *args: list,
        **kwargs: dict,
    ) -> None:
        self.db_session: AsyncSession = db_session
