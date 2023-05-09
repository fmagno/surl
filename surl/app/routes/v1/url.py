from typing import List

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as  # Body,; HTTPException,
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.session import get_db

# from app.core.config import settings
from app.schemas.url import UrlDb, UrlDbList, UrlDbRead, UrlRouteList

# from fastapi.encoders import jsonable_encoder
# from pydantic.networks import EmailStr


url_router = APIRouter()


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


# @url_router.post("/", response_model=schemas.User)
# def create_url(
#     *,
#     db: Session = Depends(deps.get_db),
#     url_in: schemas.UrlCreate,
#     current_url: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Create new user.
#     """
#     user = crud.user.get_by_email(db, email=url_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system.",
#         )
#     user = crud.user.create(db, obj_in=url_in)
#     if settings.EMAILS_ENABLED and url_in.email:
#         send_new_account_email(
#             email_to=url_in.email, username=url_in.email, password=url_in.password
#         )
#     return user


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
