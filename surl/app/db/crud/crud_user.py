import logging
import uuid
from logging import Logger
from typing import Optional

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, contains_eager

from app.db.crud.crud_base import CRUDBase
from app.schemas.session import SessionDb
from app.schemas.user import UserDb, UserDbCreate, UserDbList, UserDbUpdate
from app.schemas.oauth import TokenDb

logger: Logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[UserDb, UserDbCreate, UserDbUpdate, UserDbList]):
    async def get_by_session_id(
        self,
        db: AsyncSession,
        session_id: uuid.UUID,
    ) -> Optional[UserDb]:
        stmt = (
            select(UserDb)
            .join(SessionDb, UserDb.id == SessionDb.user_id)
            .where(SessionDb.id == session_id)
            .options(joinedload(UserDb.sessions))
        )
        result = await db.execute(stmt)
        entry = result.scalars().unique().one_or_none()
        return entry

    async def create_with_sessions(
        self,
        db: AsyncSession,
        obj_in: UserDbCreate,
        sessions: list[SessionDb],
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> UserDb:
        user: UserDb = await self.create(
            db=db,
            obj_in=obj_in,
            flush=False,
        )
        user.sessions = sessions

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await db.refresh(user)

        return user

    async def get_with_tokens_ordered_by_created_at(
        self,
        db: AsyncSession,
        id: uuid.UUID,
    ) -> UserDb:
        t = aliased(TokenDb)
        stmt = (
            select(UserDb)
            .join(t, UserDb.id == t.user_id, isouter=True)
            .where(UserDb.id == id)
            .options(contains_eager(UserDb.tokens, alias=t))
            .order_by(t.created_at.desc())
        )

        result: Result = await db.execute(stmt)
        entry: UserDb = result.unique().scalar_one_or_none()

        return entry

    async def get_by_email_with_urls(
        self,
        db: AsyncSession,
        email: str,
    ) -> UserDb:
        stmt: Select = (
            select(UserDb)
            .join(UserDb.urls, isouter=True)
            .where(UserDb.email == email)
            .options(contains_eager(UserDb.urls))
        )
        result: Result = await db.execute(stmt)
        entry = result.unique().scalar_one_or_none()
        return entry

    async def get_or_create_with_urls(
        self,
        db: AsyncSession,
        obj_in: UserDbCreate,
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> UserDb:
        user: UserDb = await self.get_by_email_with_urls(
            db=db,
            email=obj_in.email,
        )
        if not user:
            user = await self.create(
                db=db,
                obj_in=obj_in,
                flush=flush,
                commit=commit,
                refresh=refresh,
            )
        return user


crud_user = CRUDUser(UserDb, UserDbList)
