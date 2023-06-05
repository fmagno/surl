from typing import Optional

import httpx
from httpx import AsyncClient, Response
from pydantic import parse_obj_as

from app.exceptions.oauth import GithubUserEmailsNotFoundException

from .schemas import Token, User, UserEmail
import requests


async def get_access_token(
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


async def get_user(
    token: Token,
) -> Optional[User]:
    async with AsyncClient(base_url="https://api.github.com") as ac:
        response: Response = await ac.get(
            "/user",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"{token.token_type.capitalize()} {token.access_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    if response.status_code != httpx.codes.OK:
        return None

    response_payload = response.json()
    user: User = User.parse_obj(response_payload)

    return user


async def get_user_emails(
    token: Token,
) -> Optional[list[UserEmail]]:
    async with AsyncClient(base_url="https://api.github.com") as ac:
        response: Response = await ac.get(
            "/user/emails",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"{token.token_type.capitalize()} {token.access_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    if response.status_code != httpx.codes.OK:
        return None

    response_payload = response.json()
    user_emails: list[UserEmail] = parse_obj_as(list[UserEmail], response_payload)

    return user_emails
