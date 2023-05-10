import datetime as dt
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.schemas.auth import TokenPayload

settings: Settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: dt.timedelta = None
) -> str:
    if expires_delta:
        expire: dt.datetime = dt.datetime.utcnow() + expires_delta
    else:
        expire = dt.datetime.utcnow() + dt.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# def encode_token(token_payload: TokenPayload) -> str:
#     if token_payload.exp is None:
#         token_payload.exp = dt.datetime.utcnow() + dt.timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     token = jwt.encode(token_payload.dict(), settings.SECRET_KEY, algorithm=ALGORITHM)
#     return token


def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        token_data = None
    return token_data
