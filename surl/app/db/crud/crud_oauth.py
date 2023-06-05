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
    ...


crud_oauth = CRUDOAuth(TokenDb, TokenDbList)
