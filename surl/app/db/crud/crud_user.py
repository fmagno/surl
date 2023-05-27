import logging
import uuid
from logging import Logger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.crud.crud_base import CRUDBase
from app.schemas.session import SessionDb
from app.schemas.user import UserDb, UserDbCreate, UserDbList, UserDbUpdate
from sqlalchemy.orm import joinedload


logger: Logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[UserDb, UserDbCreate, UserDbUpdate, UserDbList]):
    async def get_by_session_id(
        self,
        db: AsyncSession,
        session_id: uuid.UUID,
    ) -> Optional[UserDb]:
        stmt = (
            # select(UserDb)
            # .join(UserDb.sessions)
            # .where(SessionDb.id == session_id)
            select(UserDb)
            .options(joinedload(UserDb.sessions, innerjoin=True))
            .where(SessionDb.id == session_id)
        )

        # stmt = select(UserDb, SessionDb).where(SessionDb.id == session_id)
        result = await db.execute(stmt)
        # entry = result.scalars().one_or_none()
        entry = result.scalars().unique().one_or_none()
        # entry = result.scalar_one_or_none()
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


crud_user = CRUDUser(UserDb, UserDbList)
