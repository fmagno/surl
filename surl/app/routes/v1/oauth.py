from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import timedelta
from http import client
from typing import Optional
from uuid import UUID, uuid4

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
) -> RedirectResponse:
    """"""
    # construct redirect URL for the authorisation server with:
    #   - redirect URL to the endpoint responsible for code - token exchange
    #   - client_id

    client_id: str = "CLIENT_ID"
    redirect_uri: str = "https://surl.loca.lt/api/v1/oauth/code"
    login: str = ""
    scope: str = "read:user user:email"
    state: str = urlsafe_b64encode(
        State(next="https://github.com/api/docs", salt="01010101010").json().encode()
    ).decode()
    allow_signup: bool = True

    github_authorize_url: str = (
        # github
        f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&login={login}"
        f"&scope={scope}"
        f"&state={state}"
        f"&allow_signup={allow_signup}"
    )

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
    code: str,
    state: str,
    # form_data: OAuth2ClientCredentialsRequestForm = Depends(),
    # basic_auth_user_pass: Optional[HTTPBasicCredentials] = Depends(basic_auth_token),
) -> RedirectResponse:
    """"""
    # construct redirect URL for the authorisation server with:
    #   - redirect URL to the endpoint responsible for code - token exchange
    #   - client_id

    s: State = State.parse_raw(urlsafe_b64decode(state.encode()).decode())
    token = await get_oauth2_access_token(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        code=code,
        redirect_uri="https://surl.loca.lt/api/v1/oauth/code",
    )

    # print(request.headers)

    return ""
    # return RedirectResponse(
    #     github_authorize_url,
    # )


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
