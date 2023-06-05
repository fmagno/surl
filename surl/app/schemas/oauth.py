from dataclasses import dataclass
import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel, Extra
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.user import UserDb


class State(BaseModel):
    user_id: uuid.UUID


class Token(BaseModel):
    access_token: str
    scope: str
    token_type: str


class TokenDbCreate(BaseModel):
    access_token_encrypted: str
    scope: str
    token_type: str
    expires_in: float


class TokenDbUpdate(BaseModel):
    ...


class TokenDb(Base):
    __tablename__: str = "token"

    access_token_encrypted: Mapped[str]
    token_type: Mapped[str]
    scope: Mapped[str]
    expires_in: Mapped[float]

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"),
        default=None,
        nullable=True,
    )
    user: Mapped["UserDb"] = relationship(
        back_populates="tokens",
    )


@dataclass
class TokenDbList:
    count: int
    data: list[TokenDb]
