import datetime as dt
import random
import string
from typing import Optional
import uuid
from pydantic import parse_obj_as

from dataclasses import asdict
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.crud.crud_user import crud_user
from app.exceptions.url import CreateUrlUserNotFoundError
from app.schemas.url import (
    UrlDb,
    UrlDbCreate,
    UrlRouteCreate,
    UrlRouteList,
    UrlRouteRetrieve,
)
from app.schemas.user import UserDb, UserDbRead
from app.services.base import BaseService

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

    async def get_urls_by_user_id(
        self,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: Optional[int] = None,
    ) -> UrlRouteList:
        urls_db = await crud_url.get_multi_by_user_id(
            db=self.db,
            user_id=user_id,
            skip=skip,
            limit=limit,
        )

        urls = UrlRouteList.parse_url_db_list(urls_db)
        return urls


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
