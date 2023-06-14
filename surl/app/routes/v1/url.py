from typing import Optional
from fastapi import APIRouter, Depends

from app.core.exceptions import HTTP400BadRequestException
from app.deps.url import UrlService, get_url_service
from app.exceptions.url import CreateUrlUserNotFoundError
from app.exceptions.user import CreateUserSessionNotFoundError
from app.schemas.url import UrlRouteCreate, UrlRouteList, UrlRouteRetrieve
from app.deps.user import get_or_create_user
from app.schemas.user import UserDb

url_router = APIRouter()


@url_router.post("", response_model=UrlRouteRetrieve)
async def create_url(
    *,
    url_svc: UrlService = Depends(get_url_service),
    url: UrlRouteCreate,
) -> UrlRouteRetrieve:
    """Create new url."""

    try:
        url_route_retrieve: UrlRouteRetrieve = await url_svc.create_url(
            url=url,
        )
    except CreateUrlUserNotFoundError:
        raise HTTP400BadRequestException()
    except CreateUserSessionNotFoundError:
        raise HTTP400BadRequestException()

    return url_route_retrieve


@url_router.get("", response_model=UrlRouteList)
async def list_urls_by_user_id(
    # db: AsyncSession = Depends(get_db),
    # user_id: uuid.UUID,
    *,
    url_svc: UrlService = Depends(get_url_service),
    user: UserDb = Depends(get_or_create_user),
    skip: int = 0,
    limit: Optional[int] = None,
) -> UrlRouteList:
    """
    List urls.
    """

    urls: UrlRouteList = await url_svc.get_urls_by_user_id(
        user_id=user.id,
        skip=skip,
        limit=limit,
    )
    return urls


# @url_router.put("/me", response_model=schemas.User)
# def update_url_me(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_url: models.User = Depends(deps.get_current_active_url),
# ) -> Any:
#     """
#     Update own user.
#     """
#     current_url_data = jsonable_encoder(current_url)
#     url_in = schemas.UserUpdate(**current_url_data)
#     if password is not None:
#         url_in.password = password
#     if full_name is not None:
#         url_in.full_name = full_name
#     if email is not None:
#         url_in.email = email
#     user = crud.user.update(db, db_obj=current_url, obj_in=url_in)
#     return user


# @url_router.get("/me", response_model=schemas.User)
# def retrieve_url_me(
#     db: Session = Depends(deps.get_db),
#     current_url: models.User = Depends(deps.get_current_active_url),
# ) -> Any:
#     """
#     Get current user.
#     """
#     return current_url


# @url_router.get("/{url_id}", response_model=schemas.User)
# def retrieve_url(
#     url_id: int,
#     current_url: models.User = Depends(deps.get_current_active_url),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Get a specific user by id.
#     """
#     user = crud.user.get(db, id=url_id)
#     if user == current_url:
#         return user
#     if not crud.user.is_superuser(current_url):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return user


# @url_router.put("/{url_id}", response_model=schemas.User)
# def update_url(
#     *,
#     db: Session = Depends(deps.get_db),
#     url_id: int,
#     url_in: schemas.UserUpdate,
#     current_url: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update a user.
#     """
#     user = crud.user.get(db, id=url_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.user.update(db, db_obj=user, obj_in=url_in)
#     return user
