import logging
import uuid
from logging import Logger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

# from sqlmodel import func
from sqlalchemy.sql.expression import func


from app.db.crud.crud_base import CRUDBase
from app.schemas.url import UrlDb, UrlDbCreate, UrlDbList, UrlDbUpdate

from sqlalchemy.future import select


logger: Logger = logging.getLogger(__name__)


class CRUDUrl(CRUDBase[UrlDb, UrlDbCreate, UrlDbUpdate, UrlDbList]):
    async def get_multi_by_user_id(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: Optional[int] = None,
    ) -> UrlDbList:
        stmt_count = (
            select(func.count()).select_from(self.model).where(UrlDb.user_id == user_id)
        )
        result = await db.execute(stmt_count)
        count = result.scalar_one()

        stmt = select(self.model).where(UrlDb.user_id == user_id).offset(skip)

        if limit:
            stmt = stmt.limit(limit)
        result = await db.execute(stmt)
        entries = result.scalars().all()
        return self.list_model(data=entries, count=count)


crud_url = CRUDUrl(UrlDb, UrlDbList)
