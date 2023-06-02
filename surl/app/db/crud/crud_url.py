import logging
import uuid
from logging import Logger
from typing import Optional

from sqlalchemy import Select, Selectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func

from app.db.crud.crud_base import CRUDBase
from app.schemas.url import UrlDb, UrlDbCreate, UrlDbList, UrlDbUpdate
from app.schemas.user import UserDb, UserDbCreate

logger: Logger = logging.getLogger(__name__)


class CRUDUrl(CRUDBase[UrlDb, UrlDbCreate, UrlDbUpdate, UrlDbList]):
    async def get_multi_by_user_id(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: Optional[int] = None,
    ) -> UrlDbList:
        stmt: Select = (
            select(UrlDb)
            .join(UrlDb.users)
            .where(
                UserDb.id == user_id,
            )
        )

        stmt_count = (
            select(func.count())
            .select_from(UrlDb)
            .join(UrlDb.users)
            .where(
                UserDb.id == user_id,
            )
        )

        # stmt_count = (
        #     select(func.count())
        #     .select_from(self.model)
        #     .where(
        #         user_id
        #         # user_id in UrlDb.users
        #         # UrlDb.user_id == user_id,
        #     )
        # )
        count_result = await db.execute(stmt_count)
        count = count_result.scalar_one()

        # stmt = select(self.model).where(UrlDb.user_id == user_id).offset(skip)

        if limit:
            stmt = stmt.limit(limit)
        result = await db.execute(stmt)
        entries = result.scalars().all()
        return self.list_model(data=entries, count=count)

    async def create_with_users(
        self,
        db: AsyncSession,
        obj_in: UrlDbCreate,
        users: list[UserDb],
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> UrlDb:
        url: UrlDb = await self.create(
            db=db,
            obj_in=obj_in,
            flush=False,
        )
        url.users = users

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await db.refresh(users)

        return url


crud_url = CRUDUrl(UrlDb, UrlDbList)
