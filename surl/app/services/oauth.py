import datetime as dt
import random
import string
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.crud.crud_user import crud_user
from app.exceptions.url import CreateUrlUserNotFoundError
from app.schemas.url import UrlDb, UrlDbCreate, UrlRouteCreate, UrlRouteRetrieve
from app.schemas.user import UserDb, UserDbRead
from app.services.base import BaseService


class OAuthService(BaseService):
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db=db)

    ...


# Facade #############################


async def create_oauth_service(
    db: AsyncSession,
) -> OAuthService:
    oauth_svc: OAuthService = OAuthService(db=db)
    return oauth_svc
