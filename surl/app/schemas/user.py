import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Extra

# from sqlmodel import Relationship, SQLModel

from app.schemas.base import Base
from app.schemas.url_user import UrlUserLinkDb
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from app.schemas.session import SessionDb
    from app.schemas.url import UrlDb


class UserBase(BaseModel):
    name: str
    email: Optional[str] = None

    class Config:
        orm_mode = True


# DB schemas


class UserDbRead(UserBase):
    id: uuid.UUID


class UserDbCreate(UserBase, extra=Extra.forbid):
    ...


class UserDbUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]


class UserDbList(BaseModel):
    count: int
    data: list[UserDbRead]


class UserDb(Base):
    __tablename__ = "user"

    name: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)

    sessions: Mapped[list["SessionDb"]] = relationship(
        back_populates="user",
    )

    urls: Mapped[list["UrlDb"]] = relationship(
        back_populates="users",
        secondary=UrlUserLinkDb,
    )


# Routing schemas


class UserRouteRetrieve(UserDbRead):
    ...


class UserRouteList(BaseModel):
    data: list[UserRouteRetrieve]
    count: int


class UserRouteUpdate(BaseModel):
    name: str
