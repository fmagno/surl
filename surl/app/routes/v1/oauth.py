import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from itsdangerous.url_safe import URLSafeSerializer
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


oauth_router = APIRouter()
settings: Settings = get_settings()


@oauth_router.get(
    "/login",
    include_in_schema=True,
)
async def login(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserDbRead = Depends(get_or_create_user),
) -> RedirectResponse:
    """"""
    login: str = ""
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
) -> RedirectResponse:
    """"""
    # s: State = State.parse_raw(urlsafe_b64decode(state.encode()).decode())
    serializer = URLSafeSerializer(
        secret_key=settings.SECRET_KEY,
        salt="oauth",
    )
    state_decrypted: State = State.parse_raw(serializer.loads(state))
    user_id: uuid.UUID = state_decrypted.user_id

    user_db: UserDb = await crud_user.get_with_tokens_ordered_by_created_at(
        db=db,
        id=user_id,
    )
    if not user_db:
        raise UserNotFoundException

    if user_db.tokens:
        return RedirectResponse(
            "https://surl.loca.lt/api/docs",
        )

    gh_token: Optional[GithubToken] = await get_access_token(
        client_id=settings.GITHUB_OAUTH_CLIENT_ID,
        client_secret=settings.GITHUB_OAUTH_CLIENT_SECRET,
        code=code,
        redirect_uri=settings.GITHUB_OAUTH_CODE_REDIRECT_URI,
    )
    if not gh_token:
        raise TokenNotRetrievedException

    token: Token = Token(**gh_token.dict())
    serializer = URLSafeSerializer(
        secret_key=settings.SECRET_KEY,
        salt="oauth",
    )
    access_token_encrypted: str = str(
        serializer.dumps(token.access_token),
    )
    await crud_oauth.create(
        db=db,
        obj_in=TokenDbCreate(
            **token.dict(),
            access_token_encrypted=access_token_encrypted,
            expires_in=1,
        ),
        flush=False,
    )

    gh_user: Optional[User] = await get_user(gh_token)
    if not gh_user:
        raise GithubUserNotFoundException

    gh_user_emails: Optional[list[UserEmail]] = await get_user_emails(gh_token)
    if not gh_user_emails:
        raise GithubUserEmailsNotFoundException

    gh_user_public_email: Optional[UserEmail] = next(
        (email for email in gh_user_emails if email.visibility == "public"),
        None,
    )
    if not gh_user_public_email:
        raise GithubUserPublicEmailNotFoundException

    auth_user: UserDb = await crud_user.create(
        db=db,
        obj_in=UserDbCreate(
            name=gh_user.name,
            email=gh_user_public_email.email,
        ),
        flush=False,
    )

    urls: UrlDbList = await crud_url.get_multi_by_user_id(
        db=db,
        user_id=user_id,
    )
    auth_user.urls = urls.data

    # TODO: update session to point to the user
    # await crud_session.update(db=db,)
    # user_db.sessions

    await db.commit()

    return RedirectResponse(
        "https://surl.loca.lt/api/docs",
    )
