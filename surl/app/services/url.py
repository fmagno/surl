import datetime as dt
import random
import string
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.crud.crud_user import crud_user
from app.db.session import get_db
from app.exceptions.url import CreateUrlUserNotFoundError
from app.schemas.url import UrlDb, UrlDbCreate, UrlRouteCreate, UrlRouteRetrieve
from app.schemas.user import UserDb, UserDbRead
from app.services.base import BaseService
from app.services.user import get_or_create_user

ALPHABET: str = string.ascii_lowercase + string.digits


def gen_short_uuid() -> str:
    return "".join(random.choices(ALPHABET, k=8))


class UrlService(BaseService):
    def __init__(
        self,
        db: AsyncSession,
        user: UserDbRead,
    ) -> None:
        super().__init__(db=db)
        self.user: UserDbRead = user

    async def create_url(
        self,
        url: UrlRouteCreate,
    ) -> UrlRouteRetrieve:
        user_db: Optional[UserDb] = await crud_user.get(
            db=self.db,
            id=self.user.id,
        )
        if not user_db:
            raise CreateUrlUserNotFoundError()

        url_db: UrlDb = await crud_url.create_with_users(
            db=self.db,
            obj_in=UrlDbCreate(
                **url.dict(),
                short=gen_short_uuid(),
                added_at=dt.datetime.now(),
            ),
            users=[user_db],
            commit=True,
        )

        url_route_retrieve: UrlRouteRetrieve = UrlRouteRetrieve.parse_url_db(
            url_db=url_db
        )
        return url_route_retrieve


# Facade #############################


async def create_url_service(
    db: AsyncSession,
    user: UserDbRead,
) -> UrlService:
    url_svc: UrlService = UrlService(
        db=db,
        user=user,
    )
    return url_svc


# Injectable Dependencies ############


async def get_url_service(
    db: AsyncSession = Depends(get_db),
    user: UserDbRead = Depends(get_or_create_user),
) -> UrlService:
    url_svc: UrlService = await create_url_service(
        db=db,
        user=user,
    )
    return url_svc
