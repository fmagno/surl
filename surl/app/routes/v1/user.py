import uuid
from typing import List

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as  # Body,; HTTPException,
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.crud.crud_user import crud_user
from app.db.session import get_db
from app.schemas import user
from app.schemas.url import UrlDbList, UrlRouteList, UrlRouteRetrieve

# from app.core.config import settings
from app.schemas.user import UserDb, UserDbList, UserDbRead, UserRouteList

# from fastapi.encoders import jsonable_encoder
# from pydantic.networks import EmailStr


user_router = APIRouter()


@user_router.get("/", response_model=UserRouteList)
async def list_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> UserRouteList:
    """List users."""

    try:
        users_db: UserDbList = await crud_user.get_multi(db, skip=skip, limit=limit)
        users: UserRouteList = parse_obj_as(UserRouteList, users_db)
    except Exception as e:
        raise e

    return users


@user_router.get("/{user_id}/urls", response_model=UrlRouteList)
async def list_urls(
    db: AsyncSession = Depends(get_db),
    *,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 10,
) -> UrlRouteList:
    """List urls by user_id."""

    # TODO: Deal with authentication/authorisation

    try:
        urls_db: UrlDbList = await crud_url.get_multi_by_user_id(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
        )
        # urls: UrlRouteList = parse_obj_as(UrlRouteList, urls_db)
        urls: UrlRouteList = UrlRouteList(
            count=urls_db.count,
            data=[UrlRouteRetrieve(**u.dict(), users=[user_id]) for u in urls_db.data],
        )

    except Exception as e:
        raise e

    return urls


# @user_router.post("/", response_model=schemas.User)
# def create_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: schemas.UserCreate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Create new user.
#     """
#     user = crud.user.get_by_email(db, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system.",
#         )
#     user = crud.user.create(db, obj_in=user_in)
#     if settings.EMAILS_ENABLED and user_in.email:
#         send_new_account_email(
#             email_to=user_in.email, username=user_in.email, password=user_in.password
#         )
#     return user


# @user_router.put("/me", response_model=schemas.User)
# def update_user_me(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update own user.
#     """
#     current_user_data = jsonable_encoder(current_user)
#     user_in = schemas.UserUpdate(**current_user_data)
#     if password is not None:
#         user_in.password = password
#     if full_name is not None:
#         user_in.full_name = full_name
#     if email is not None:
#         user_in.email = email
#     user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
#     return user


# @user_router.get("/me", response_model=schemas.User)
# def retrieve_user_me(
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get current user.
#     """
#     return current_user


# @user_router.get("/{user_id}", response_model=schemas.User)
# def retrieve_user(
#     user_id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Get a specific user by id.
#     """
#     user = crud.user.get(db, id=user_id)
#     if user == current_user:
#         return user
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return user


# @user_router.put("/{user_id}", response_model=schemas.User)
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: int,
#     user_in: schemas.UserUpdate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update a user.
#     """
#     user = crud.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.user.update(db, db_obj=user, obj_in=user_in)
#     return user
