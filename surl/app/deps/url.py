import datetime as dt
import random
import string

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps.user import get_or_create_user
from app.schemas.user import UserDbRead
from app.services.url import UrlService, create_url_service


async def get_url_service(
    db: AsyncSession = Depends(get_db),
    user: UserDbRead = Depends(get_or_create_user),
) -> UrlService:
    url_svc: UrlService = await create_url_service(
        db=db,
        user=user,
    )
    return url_svc
