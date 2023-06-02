from typing import Optional

import httpx
from httpx import AsyncClient, Response

from .schemas import Token


async def get_oauth2_access_token(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
) -> Optional[Token]:
    async with AsyncClient(
        base_url=f"https://github.com/login/oauth/access_token"
    ) as ac:
        response: Response = await ac.post(
            "",
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={
                "Accept": "application/json",
            },
        )
    if response.status_code != httpx.codes.OK:
        return None

    response_payload = response.json()
    token: Token = Token.parse_obj(response_payload)

    return token
