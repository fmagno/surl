import logging
from typing import Any, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import Settings, get_settings
from app.db.crud.crud_user import crud_user
from app.db.session import get_db
from app.schemas.auth import TokenPayload
from app.schemas.user import UserDb
from app.services.base import BaseService

settings: Settings = get_settings()
logger: logging.Logger = logging.getLogger(__name__)


class UserService(BaseService):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db=db)


# Facade #############################


async def create_service(db: AsyncSession) -> UserService:
    user_svc = UserService(db)
    return user_svc


# Injectable Dependencies ############


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_svc: UserService = await create_service(db)
    return user_svc


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/token",
)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> UserDb:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise

    user: Optional[UserDb] = await crud_user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
