import datetime as dt
import random
import string
from typing import Optional
import uuid
from fastapi import Request
from itsdangerous import URLSafeSerializer

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_url import crud_url
from app.db.crud.crud_user import crud_user
from app.exceptions.url import CreateUrlUserNotFoundError
from app.schemas.url import (
    UrlDb,
    UrlDbCreate,
    UrlDbList,
    UrlRouteCreate,
    UrlRouteRetrieve,
)
from app.schemas.user import UserDb, UserDbCreate, UserDbRead
from app.services.base import BaseService
from app.core.config import Settings, get_settings
from app.schemas.oauth import State
from app.exceptions.oauth import (
    GithubUserEmailsNotFoundException,
    GithubUserNotFoundException,
    GithubUserPublicEmailNotFoundException,
    TokenNotRetrievedException,
    UserNotFoundException,
)
from fastapi.responses import RedirectResponse
from app.utils.github_client import (
    get_access_token,
    Token as GithubToken,
    get_user,
    get_user_emails,
)
from app.schemas.oauth import State, Token, TokenDbCreate
from app.db.crud.crud_oauth import crud_oauth
from app.db.crud.crud_session import crud_session
from app.exceptions.session import SessionNotFoundException
from app.schemas.session import SessionDb
from app.utils.github_client.schemas import User, UserEmail


settings: Settings = get_settings()


class OAuthService(BaseService):
    def __init__(
        self,
        db: AsyncSession,
        user: UserDbRead,
        request: Request,
    ) -> None:
        super().__init__(db=db)
        self.user: UserDbRead = user
        self.request: Request = request

        self.serializer = URLSafeSerializer(
            secret_key=settings.SECRET_KEY,
            salt="oauth",
        )

    async def login(
        self,
    ) -> str:
        login: str = ""
        state_encrypted: str = str(
            self.serializer.dumps(
                State(user_id=self.user.id).json(),
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

        await self.db.commit()
        return github_authorize_url

    async def code(
        self,
        code: str,
        state: str,
    ) -> str:
        state_decrypted: State = State.parse_raw(self.serializer.loads(state))
        user_id: uuid.UUID = state_decrypted.user_id

        user_db: UserDb = await crud_user.get_with_tokens_ordered_by_created_at(
            db=self.db,
            id=user_id,
        )
        if not user_db:
            raise UserNotFoundException

        if user_db.tokens:
            return "https://surl.loca.lt/api/docs"

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
            db=self.db,
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
            db=self.db,
            obj_in=UserDbCreate(
                name=gh_user.name,
                email=gh_user_public_email.email,
            ),
            flush=False,
        )

        urls: UrlDbList = await crud_url.get_multi_by_user_id(
            db=self.db,
            user_id=user_id,
        )
        auth_user.urls = urls.data

        session_id: uuid.UUID = self.request.session["surl_session"]
        session_db: Optional[SessionDb] = await crud_session.get(
            db=self.db,
            id=session_id,
        )
        if not session_db:
            raise SessionNotFoundException

        session_db.user = auth_user
        self.db.add(session_db)

        await self.db.commit()

        return "https://surl.loca.lt/api/docs"


# Facade #############################


async def create_oauth_service(
    db: AsyncSession,
    user: UserDbRead,
    request: Request,
) -> OAuthService:
    oauth_svc: OAuthService = OAuthService(
        db=db,
        user=user,
        request=request,
    )
    return oauth_svc
