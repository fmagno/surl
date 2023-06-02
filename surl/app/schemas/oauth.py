import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel
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


class TokenDb(Base):
    __tablename__: str = "token"

    access_token_encrypted: Mapped[str]
    token_type: Mapped[str]
    expires_in: Mapped[float]

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"),
        default=None,
        nullable=True,
    )
    user: Mapped["UserDb"] = relationship(
        back_populates="tokens",
    )
