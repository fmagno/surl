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
from app.schemas.oauth import TokenDb, TokenDbCreate, TokenDbList, TokenDbUpdate

logger: Logger = logging.getLogger(__name__)


class CRUDOAuth(
    CRUDBase[
        TokenDb,
        TokenDbCreate,
        TokenDbUpdate,
        TokenDbList,
    ]
):
    async def create_with_user(
        self,
        db: AsyncSession,
        obj_in: TokenDbCreate,
        user: UserDb,
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> TokenDb:
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = TokenDb(**obj_in.dict(), user=user)
        db.add(db_obj)

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await db.refresh(db_obj)

        return db_obj


crud_oauth = CRUDOAuth(TokenDb, TokenDbList)
