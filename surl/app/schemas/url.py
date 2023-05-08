import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import Extra
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.user import UserDb


class UrlBase(SQLModel):
    alias: str
    target: str
    is_private: bool
    expiry_period: int
    added_at: dt.datetime


class UrlDbRead(UrlBase):
    id: uuid.UUID


class UrlDbCreate(UrlBase, extra=Extra.forbid):
    ...


class UrlDbUpdate(SQLModel):
    short_url: Optional[str]
    target_url: Optional[str]
    is_private: Optional[bool]
    expiry_period: Optional[int]
    added_at: Optional[dt.datetime]


class UrlDb(Base, UrlBase, table=True):
    __tablename__ = "url"

    added_at: dt.datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    user: "UserDb" = Relationship(back_populates="urls")
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")
