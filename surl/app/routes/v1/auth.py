from datetime import timedelta
from typing import Optional

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

auth_router = APIRouter()
settings: Settings = get_settings()


@auth_router.post(
    "/token",
    response_model=Token,
    include_in_schema=False,
)
async def login_access_token(
    form_data: OAuth2ClientCredentialsRequestForm = Depends(),
    basic_auth_user_pass: Optional[HTTPBasicCredentials] = Depends(basic_auth_token),
) -> Token:
    """OAuth2 compatible token login, get an access token for future requests."""
    if form_data.client_id and form_data.client_secret:
        client_id, client_secret = form_data.client_id, form_data.client_secret
    elif basic_auth_user_pass:
        client_id, client_secret = (
            basic_auth_user_pass.username,
            basic_auth_user_pass.password,
        )
    else:
        raise HTTP401UnauthorizedException()

    sett_key, sett_secret = settings.API_CLIENT_KEY, settings.API_CLIENT_SECRET
    if (client_id, client_secret) != (sett_key, sett_secret):
        raise HTTP401UnauthorizedException()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            client_id, expires_delta=access_token_expires
        ),
        token_type="bearer",
        expires_in=access_token_expires.total_seconds(),
    )


@auth_router.post(
    "/test-token",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTP401UnauthorizedContent,
            "description": "Not authenticated",
        },
    },
)
async def test_token(
    auth_token_payload: TokenPayload = Depends(oauth2_token_payload),
) -> Response:
    """Test access token."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)
