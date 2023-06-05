import datetime as dt
import random
import string

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.url import UrlService, create_url_service
from surl.app.services.oauth import OAuthService


async def get_oauth_service(
    db: AsyncSession = Depends(get_db),
) -> OAuthService:
    oauth_svc: UrlService = await create_url_service(db=db)
    return oauth_svc
