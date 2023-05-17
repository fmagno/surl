from datetime import timedelta
from typing import Optional
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Response, status
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
from fastapi.responses import RedirectResponse

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

    client_id: str = ""
    redirect_uri: str = ""
    code_challenge: str = ""
    code_challenge_method: str = ""
    twitter_authorize_url: str = (
        # github
        # f"https://github.com/login/oauth/authorize"
        # f"?client_id={client_id}"
        # f"&redirect_uri={redirect_uri}"
        # f"&login={login}"
        # f"&scope={scope}"
        # f"&state={state}"
        # f"&allow_signup={allow_signup}"
        #
        # twitter
        "https://twitter.com/i/oauth2/authorize"
        "?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge={code_challenge_method}"
    )

    return RedirectResponse(
        twitter_authorize_url,
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
