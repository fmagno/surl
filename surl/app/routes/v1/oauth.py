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
from app.exceptions.oauth import UserNotFoundException
from app.schemas.oauth import State, Token
from app.schemas.url import UrlDbList
from app.schemas.user import UserDb, UserDbCreate, UserDbRead
from app.utils.github_client import get_oauth2_access_token, Token as GithubToken


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
    # user_db: Optional[UserDb] = await crud_user.get(
    #     db=db,
    #     id=user_id,
    # )

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

    github_token: GithubToken = await get_oauth2_access_token(
        client_id=settings.GITHUB_OAUTH_CLIENT_ID,
        client_secret=settings.GITHUB_OAUTH_CLIENT_SECRET,
        code=code,
        redirect_uri=settings.GITHUB_OAUTH_CODE_REDIRECT_URI,
    )
    token: Token = Token(**github_token.dict())

    #

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
