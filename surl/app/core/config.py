import secrets
from functools import lru_cache
from typing import List

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    DEBUG: bool = False

    PROJECT_NAME: str = "surl"
    API_V1_STR: str = "/api/v1"
    API_APP: str = "app.main:app"
    # SERVER_HOSTNAME: str
    PORT: int = 9000

    API_CLIENT_KEY: str
    API_CLIENT_SECRET: str

    # CORS_ORIGINS is a str comma separated origins
    # e.g: "http://localhost,http://localhost:9000,http://localhost:8008"
    CORS_ORIGINS: str = ""

    @validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        raise ValueError(v)

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_URL: str
    # TEST_DATABASE_URL: Optional[str] = None

    GITHUB_OAUTH_CLIENT_ID: str
    GITHUB_OAUTH_CLIENT_SECRET: str
    GITHUB_OAUTH_SCOPE: str
    GITHUB_OAUTH_CODE_REDIRECT_URI: str
    GITHUB_OAUTH_AUTHORIZE_REDIRECT_URI: str
    GITHUB_OAUTH_ALLOW_SIGNUP: bool

    SESSION_MAX_AGE: int

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
