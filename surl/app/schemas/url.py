import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Extra
from sqlmodel import (
    Column,
    DateTime,
    Field,
    Relationship,
    SQLModel,
    func,
)

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.user import UserDb


class UrlBase(SQLModel):
    short: str
    target: str
    is_private: bool
    expiry_period: int
    added_at: dt.datetime


# DB schemas
class UrlDbRead(UrlBase):
    id: uuid.UUID


class UrlDbCreate(UrlBase, extra=Extra.forbid):
    ...


class UrlDbUpdate(SQLModel):
    short: Optional[str]
    target: Optional[str]
    is_private: Optional[bool]
    expiry_period: Optional[int]
    added_at: Optional[dt.datetime]


class UrlDbList(BaseModel):
    count: int
    data: list[UrlDbRead]


class UrlDb(Base, UrlBase, table=True):
    __tablename__ = "url"

    added_at: dt.datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    user: "UserDb" = Relationship(back_populates="urls")
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")


# Routing schemas


class UrlRouteCreate(BaseModel):
    target: str
    is_private: bool
    expiry_period: int


class UrlRouteRetrieve(UrlDbRead):
    user_id: uuid.UUID


class UrlRouteList(BaseModel):
    count: int
    data: list[UrlRouteRetrieve]


class UrlRouteUpdate(BaseModel):
    is_private: Optional[bool]
    expiry_period: Optional[int]
