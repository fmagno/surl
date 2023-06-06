from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.oauth import OAuthService, create_oauth_service
from app.deps.user import get_or_create_user
from app.schemas.user import UserDbRead


async def get_oauth_service(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: UserDbRead = Depends(get_or_create_user),
    # user: UserDbRead = Depends(GetOrCreateUser(commit=True)),
) -> OAuthService:
    oauth_svc: OAuthService = await create_oauth_service(
        db=db,
        user=user,
        request=request,
    )
    return oauth_svc
