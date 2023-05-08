from sqlalchemy.ext.asyncio.session import AsyncSession


class BaseService:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db
