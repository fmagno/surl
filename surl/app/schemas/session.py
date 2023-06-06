from dataclasses import dataclass
import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.user import UserDb


class SessionBase(BaseModel):
    created_at: dt.datetime

    class Config:
        orm_mode = True


class SessionDbRead(SessionBase):
    id: uuid.UUID


class SessionDbCreate(SessionBase):
    created_at: dt.datetime = dt.datetime.now()


class SessionDbList(BaseModel):
    count: int
    data: list[SessionDbRead]


class SessionDb(Base):
    __tablename__ = "session"

    user: Mapped["UserDb"] = relationship(
        back_populates="sessions",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"),
        default=None,
        nullable=True,
    )


class SessionDbUpdate(BaseModel):
    ...
    # user: Optional["UserDb"]


class SessionHttp(BaseModel):
    session: SessionDbRead
    cookie: str
