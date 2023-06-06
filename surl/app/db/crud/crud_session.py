import logging
from logging import Logger
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.crud.crud_base import CRUDBase, ModelType
from app.schemas.session import (
    SessionDb,
    SessionDbCreate,
    SessionDbList,
    SessionDbUpdate,
)
from app.schemas.user import UserDb
from fastapi.encoders import jsonable_encoder


logger: Logger = logging.getLogger(__name__)


class CRUDSession(
    CRUDBase[
        SessionDb,
        SessionDbCreate,
        SessionDbUpdate,
        SessionDbList,
    ]
):
    async def get_first(
        self,
        db: AsyncSession,
    ) -> Optional[SessionDb]:
        # stmt = select(self.model).where(self.model.id == id)
        stmt = select(self.model)
        result = await db.execute(stmt)
        entry = result.scalars().first()
        return entry

    async def update_with_user(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        # obj_in: SessionDbUpdate,
        user: UserDb,
        flush: bool = True,
        commit: bool = False,
    ) -> ModelType:
        # obj_data = jsonable_encoder(db_obj)
        # if isinstance(obj_in, dict):
        #     update_data = obj_in
        # else:
        #     update_data = obj_in.dict(exclude_unset=True)
        # for field in dict(**obj_in, user=user):
        #     if field in update_data:
        #         setattr(db_obj, field, update_data[field])

        setattr(db_obj, "user", user)

        db.add(db_obj)
        if flush:
            await db.flush()
        if commit:
            await db.commit()
        return db_obj


crud_session = CRUDSession(
    SessionDb,
    SessionDbList,
)
