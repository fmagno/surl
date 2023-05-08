import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import Extra
from sqlmodel import Relationship, SQLModel

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.url import UrlDb


class UserBase(SQLModel):
    name: str
    email: str


class UserDbRead(UserBase):
    id: uuid.UUID


class UserDbCreate(UserBase, extra=Extra.forbid):
    ...


class UserDbUpdate(SQLModel):
    name: Optional[str]
    email: Optional[str]


class UserDb(Base, UserBase, table=True):
    __tablename__ = "user"

    urls: list["UrlDb"] = Relationship(back_populates="user")
