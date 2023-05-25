import datetime as dt
from typing import Optional

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.session import get_db
from app.schemas.url import (
    UrlDb,
    UrlDbCreate,
    UrlDbRead,
    UrlRouteCreate,
    UrlRouteRetrieve,
)
from app.schemas.user import UserDb, UserDbRead
from app.services.user import get_or_create_user
from app.db.crud.crud_user import crud_user
from app.exceptions.url import CreateUrlUserNotFoundError
from app.services.url import gen_short_uuid


url_router = APIRouter()


@url_router.post("", response_model=UrlRouteRetrieve)
async def create_url(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserDbRead = Depends(get_or_create_user),
    url: UrlRouteCreate,
) -> UrlRouteRetrieve:
    """Create new url."""

    user_db: Optional[UserDb] = await crud_user.get(
        db=db,
        id=user.id,
    )
    if not user_db:
        raise CreateUrlUserNotFoundError()

    url_db: UrlDb = await crud_url.create_with_user(
        db=db,
        obj_in=UrlDbCreate(
            **url.dict(),
            short=gen_short_uuid(),
            added_at=dt.datetime.now(),
        ),
        user=user_db,
        commit=True,
    )

    url_db_read = UrlRouteRetrieve(**url_db.dict())

    return url_db_read


# @url_router.get("/", response_model=UrlRouteList)
# async def list_urls_by_user_id(
#     db: AsyncSession = Depends(get_db),
#     user_id: uuid.UUID,
#     skip: int = 0,
#     limit: int = 100,
# ) -> UrlRouteList:
#     """
#     List urls.
#     """

#     try:
#         urls_db: UrlDbList = await crud_url.get_multi(db, skip=skip, limit=limit)
#         urls: UrlRouteList = parse_obj_as(UrlRouteList, urls_db)
#     except Exception as e:
#         raise e

#     return urls


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
