from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import timedelta
from http import client
from operator import attrgetter
from typing import Optional, cast
from uuid import UUID, uuid4
import uuid

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasicCredentials

from app.core import security
from app.core.auth import (
    OAuth2ClientCredentialsRequestForm,
    basic_auth_token,
    oauth2_token_payload,
)
from app.core.config import Settings, get_settings
from app.core.exceptions import HTTP401UnauthorizedException
from app.schemas.auth import Token, TokenPayload
from app.schemas.http_errors import HTTP401UnauthorizedContent
from app.schemas.oauth import State
from app.utils.github_client import get_oauth2_access_token
from app.services.session import get_or_create_session
from app.schemas.session import SessionDbRead
from app.schemas.user import UserDb, UserDbCreate, UserDbRead
from app.services.user import get_or_create_user

from itsdangerous.url_safe import URLSafeSerializer

from app.db.crud.crud_user import crud_user
from app.db.crud.crud_url import crud_url
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.url import UrlDb, UrlDbCreate, UrlDbList
from app.exceptions.oauth import UserNotFoundException

from pydantic import parse_obj_as

oauth_router = APIRouter()
settings: Settings = get_settings()


@oauth_router.get(
    "/login",
    # response_model=RedirectResponse,
    include_in_schema=True,
)
async def login(
    # form_data: OAuth2ClientCredentialsRequestForm = Depends(),
    # basic_auth_user_pass: Optional[HTTPBasicCredentials] = Depends(basic_auth_token),
    *,
    db: AsyncSession = Depends(get_db),
    user: UserDbRead = Depends(get_or_create_user),
) -> RedirectResponse:
    """"""
    login: str = ""
    # scope: str = "read:user user:email"
    # state: str = urlsafe_b64encode(
    #     State(
    #         user_id=user.id,
    #     )
    #     .json()
    #     .encode()
    # ).decode()

    serializer = URLSafeSerializer(
        secret_key=settings.SECRET_KEY,
        salt="oauth",
    )
    state_encrypted: str = str(
        serializer.dumps(
            State(user_id=user.id).json(),
        ),
    )

    github_authorize_url: str = (
        # github
        f"{settings.GITHUB_OAUTH_AUTHORIZE_REDIRECT_URI}"
        f"?client_id={settings.GITHUB_OAUTH_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_OAUTH_CODE_REDIRECT_URI}"
        f"&login={login}"
        f"&scope={settings.GITHUB_OAUTH_SCOPE}"
        f"&state={state_encrypted}"
        f"&allow_signup={settings.GITHUB_OAUTH_ALLOW_SIGNUP}"
    )

    await db.commit()

    return RedirectResponse(
        github_authorize_url,
    )


@oauth_router.get(
    "/code",
    # response_model=RedirectResponse,
    include_in_schema=True,
)
async def code(
    request: Request,
    *,
    db: AsyncSession = Depends(get_db),
    code: str,
    state: str,
    response: Response,
    # form_data: OAuth2ClientCredentialsRequestForm = Depends(),
    # basic_auth_user_pass: Optional[HTTPBasicCredentials] = Depends(basic_auth_token),
) -> RedirectResponse:
    """"""
    # s: State = State.parse_raw(urlsafe_b64decode(state.encode()).decode())
    serializer = URLSafeSerializer(
        secret_key=settings.SECRET_KEY,
        salt="oauth",
    )
    state_decrypted: State = State.parse_raw(serializer.loads(state))
    user_id: uuid.UUID = state_decrypted.user_id
    user_db: Optional[UserDb] = await crud_user.get(
        db=db,
        id=user_id,
    )
    if not user_db:
        raise UserNotFoundException

    # User is already authenticated
    # FIXME: Check user is already authenticated via token table -> user
    if user_db.email:
        return RedirectResponse(
            "https://surl.loca.lt/api/docs",
        )

    token: Optional[Token] = await get_oauth2_access_token(
        client_id=settings.GITHUB_OAUTH_CLIENT_ID,
        client_secret=settings.GITHUB_OAUTH_CLIENT_SECRET,
        code=code,
        redirect_uri=settings.GITHUB_OAUTH_CODE_REDIRECT_URI,
    )

    # create new user in db: authenticated user
    # urls = get_multi_url_by_user_id(anonymous_user.id)
    # for each url in urls: Url(**url.dict(excludes="id"))

    auth_user: UserDb = await crud_user.create(
        db=db,
        obj_in=UserDbCreate(name="auth user", email=""),
        flush=False,
    )

    urls: UrlDbList = await crud_url.get_multi_by_user_id(
        db=db,
        user_id=user_id,
    )

    auth_user.urls = urls.data

    await db.commit()

    return RedirectResponse(
        "https://surl.loca.lt/api/docs",
    )


# @auth_router.post(
#     "/test-token",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {
#             "model": HTTP401UnauthorizedContent,
#             "description": "Not authenticated",
#         },
#     },
# )
# async def test_token(
#     auth_token_payload: TokenPayload = Depends(oauth2_token_payload),
# ) -> Response:
#     """Test access token."""
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
