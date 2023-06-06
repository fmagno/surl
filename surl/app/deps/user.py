import logging
from typing import Any, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import Settings, get_settings
from app.db.crud.crud_session import crud_session
from app.db.crud.crud_user import crud_user
from app.db.session import get_db
from app.deps.session import get_or_create_session
from app.exceptions.user import CreateUserSessionNotFoundError

# from app.schemas.auth import TokenPayload
from app.schemas.session import SessionDb, SessionDbRead
from app.schemas.user import UserDb, UserDbCreate, UserDbRead
from app.services.user import UserService, create_service

settings: Settings = get_settings()
logger: logging.Logger = logging.getLogger(__name__)


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_svc: UserService = await create_service(db)
    return user_svc


# class GetOrCreateUser:
#     def __init__(
#         self,
#         flush: Optional[bool] = True,
#         commit: Optional[bool] = False,
#         refresh: Optional[bool] = False,
#     ):
#         self.flush: Optional[bool] = flush
#         self.commit: Optional[bool] = commit
#         self.refresh: Optional[bool] = refresh

#     async def __call__(
#         self,
#         db: AsyncSession = Depends(get_db),
#         session: SessionDbRead = Depends(get_or_create_session),
#     ):
#         """Returns one of:
#         - Previously authenticated user (oauth2)
#         - Previously created anonymous user
#         - A newly created anonymous user
#         """

#         user: Optional[UserDb] = await crud_user.get_by_session_id(
#             db=db,
#             session_id=session.id,
#         )
#         if not user:
#             session_db: Optional[SessionDb] = await crud_session.get(
#                 db=db,
#                 id=session.id,
#             )
#             if not session_db:
#                 raise CreateUserSessionNotFoundError()

#             user = await crud_user.create_with_sessions(
#                 db=db,
#                 obj_in=UserDbCreate(name="anonymous"),
#                 sessions=[session_db],
#             )

#         user_db_read: UserDbRead = UserDbRead.from_orm(user)

#         return user_db_read


async def get_or_create_user(
    db: AsyncSession = Depends(get_db),
    session: SessionDbRead = Depends(get_or_create_session),
) -> UserDbRead:
    """Returns one of:
    - Previously authenticated user (oauth2)
    - Previously created anonymous user
    - A newly created anonymous user
    """

    user: Optional[UserDb] = await crud_user.get_by_session_id(
        db=db,
        session_id=session.id,
    )
    if not user:
        session_db: Optional[SessionDb] = await crud_session.get(
            db=db,
            id=session.id,
        )
        if not session_db:
            raise CreateUserSessionNotFoundError()

        user = await crud_user.create_with_sessions(
            db=db,
            obj_in=UserDbCreate(name="anonymous"),
            sessions=[session_db],
        )

    user_db_read: UserDbRead = UserDbRead.from_orm(user)

    return user_db_read
