from typing import Dict, Optional, Tuple

from fastapi import Depends, Form, Request
from fastapi.openapi.models import (
    OAuthFlowAuthorizationCode,
    OAuthFlowClientCredentials,
    OAuthFlows,
)
from fastapi.security import HTTPBasic
from fastapi.security.oauth2 import OAuth2  # , OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param

from app.core import security
from app.core.config import Settings, get_settings
from app.core.exceptions import HTTP401UnauthorizedException
from app.schemas.auth import TokenPayload

settings: Settings = get_settings()


class OAuth2ClientCredentialsRequestForm:
    """
    Expect OAuth2 client credentials as form request parameters.

    Ref: RFC 6749: The OAuth 2.0 Authorization Framework
    Secion: 4.4.2. Access Token Request

    It creates the following Form request parameters in your endpoint:
    grant_type: the OAuth2 spec says it is required and MUST be the fixed string "client_credentials".
        Nevertheless, this dependency class is permissive and allows not passing it.
    scope: Optional string. Several scopes (each one a string) separated by spaces. Currently unused.
    client_id: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    client_secret: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    """

    def __init__(
        self,
        grant_type: str = Form(None, regex="^(client_credentials|refresh_token)$"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ) -> None:
        self.grant_type: str = grant_type
        self.scopes: list[str] = scope.split()
        self.client_id: Optional[str] = client_id
        self.client_secret: Optional[str] = client_secret


class OAuth2ClientCredentials(OAuth2):
    """
    Expect OAuth2 client access token ("bearer" token type).

    Ref: RFC 6749: The OAuth 2.0 Authorization Framework
    Secion: 7. Accessing Protected Resources
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
    ) -> None:
        if not scopes:
            scopes = {}
        flows = OAuthFlows(
            clientCredentials=OAuthFlowClientCredentials(
                tokenUrl=tokenUrl, scopes=scopes
            )
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=True)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: Optional[str] = request.headers.get("Authorization")
        scheme_param: Tuple[str, str] = get_authorization_scheme_param(authorization)
        scheme, param = scheme_param

        if not authorization or scheme.lower() != "bearer":
            raise HTTP401UnauthorizedException()
        return param


oauth2_token = OAuth2ClientCredentials(
    tokenUrl=f"{settings.API_V1_STR}/auth/token",
    scopes={
        "write": "write permission",
        "read": "read permission",
    },
)

basic_auth_token = HTTPBasic(auto_error=False)


async def oauth2_token_payload(token: str = Depends(oauth2_token)) -> TokenPayload:
    token_payload: Optional[TokenPayload] = security.decode_token(token)
    if not token_payload:
        raise HTTP401UnauthorizedException()
    return token_payload
