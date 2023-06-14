from fastapi import APIRouter, Depends

from app.deps.url import UrlService, get_url_service
from app.deps.user import get_or_create_user
from app.schemas.user import UserDbRead
from fastapi.responses import RedirectResponse

from app.core.exceptions import HTTP404NotFoundException


short_router = APIRouter()


@short_router.get("/{short:path}")
async def short_to_target(
    *,
    short: str,
    user: UserDbRead = Depends(get_or_create_user),
    url_svc: UrlService = Depends(get_url_service),
    # url: UrlRouteCreate,
) -> RedirectResponse:
    """Create new url."""

    # FIXME: Replace this with a method that queries the database
    # for the user_id directly
    user_urls = await url_svc.get_urls_by_user_id(
        user_id=user.id,
    )
    url = next((url for url in user_urls.data if url.short == short), None)

    if url:
        return RedirectResponse(url.target)
    raise HTTP404NotFoundException
