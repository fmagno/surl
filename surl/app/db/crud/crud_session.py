import logging
from logging import Logger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.crud.crud_base import CRUDBase, ModelType
from app.schemas.session import (
    SessionDb,
    SessionDbCreate,
    SessionDbList,
    SessionDbUpdate,
)

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


crud_session = CRUDSession(
    SessionDb,
    SessionDbList,
)
