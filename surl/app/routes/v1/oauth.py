import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from itsdangerous.url_safe import URLSafeSerializer
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.crud.crud_url import crud_url
from app.db.crud.crud_user import crud_user
from app.db.session import get_db
from app.deps.user import get_or_create_user
from app.exceptions.oauth import (
    GithubUserNotFoundException,
    GithubUserEmailsNotFoundException,
    GithubUserPublicEmailNotFoundException,
    TokenNotRetrievedException,
    UserNotFoundException,
)
from app.schemas.oauth import State, Token, TokenDbCreate
from app.schemas.url import UrlDbList
from app.schemas.user import UserDb, UserDbCreate, UserDbRead
from app.utils.github_client import (
    get_access_token,
    Token as GithubToken,
    get_user,
    get_user_emails,
)
from app.utils.github_client.schemas import (
    User,
    UserEmail,
)
from app.db.crud.crud_oauth import crud_oauth
from app.db.crud.crud_session import crud_session
from app.schemas.session import SessionDb, SessionDbUpdate
from app.exceptions.session import SessionNotFoundException
from app.deps.oauth import get_oauth_service
from app.services.oauth import OAuthService
from app.core.exceptions import HTTP400BadRequestException


oauth_router = APIRouter()
settings: Settings = get_settings()


@oauth_router.get(
    "/login",
    include_in_schema=True,
)
async def login(
    oauth_svc: OAuthService = Depends(get_oauth_service),
) -> RedirectResponse:
    """"""
    try:
        github_authorize_url = await oauth_svc.login()
    except:
        raise HTTP400BadRequestException

    return RedirectResponse(
        github_authorize_url,
    )


@oauth_router.get(
    "/code",
    # response_model=RedirectResponse,
    include_in_schema=True,
)
async def code(
    *,
    oauth_svc: OAuthService = Depends(get_oauth_service),
    code: str,
    state: str,
) -> RedirectResponse:
    """"""

    try:
        redirect_url = await oauth_svc.exchange_code_for_token(
            code=code,
            state=state,
        )
    except UserNotFoundException:
        raise HTTP400BadRequestException
    except TokenNotRetrievedException:
        raise HTTP400BadRequestException
    except GithubUserNotFoundException:
        raise HTTP400BadRequestException
    except GithubUserEmailsNotFoundException:
        raise HTTP400BadRequestException
    except GithubUserPublicEmailNotFoundException:
        raise HTTP400BadRequestException
    except SessionNotFoundException:
        raise HTTP400BadRequestException

    return RedirectResponse(redirect_url)
