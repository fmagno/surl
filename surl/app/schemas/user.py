import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Extra
from sqlmodel import Relationship, SQLModel

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.url import UrlDb
    from app.schemas.session import SessionDb


class UserBase(BaseModel):
    name: str
    email: str


# DB schemas


class UserDbRead(UserBase):
    id: uuid.UUID


class UserDbCreate(UserBase, extra=Extra.forbid):
    ...


class UserDbUpdate(SQLModel):
    name: Optional[str]
    email: Optional[str]


class UserDbList(BaseModel):
    count: int
    data: list[UserDbRead]


class UserDb(Base, UserBase, table=True):
    __tablename__ = "user"

    urls: list["UrlDb"] = Relationship(back_populates="user")
    sessions: list["SessionDb"] = Relationship(back_populates="user")


# Routing schemas


class UserRouteRetrieve(UserDbRead):
    ...


class UserRouteList(BaseModel):
    data: list[UserRouteRetrieve]
    count: int


class UserRouteUpdate(BaseModel):
    name: str
