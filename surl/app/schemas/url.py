import datetime as dt
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base import Base
from app.schemas.url_user import UrlUserLinkDb

# from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


if TYPE_CHECKING:
    from app.schemas.user import UserDb


class UrlBase(BaseModel):
    short: str
    target: str
    is_private: bool
    expiry_period: int
    added_at: dt.datetime

    class Config:
        orm_mode = True


# DB schemas
class UrlDbRead(UrlBase):
    id: uuid.UUID


class UrlDbCreate(UrlBase, extra=Extra.forbid):
    ...


class UrlDbUpdate(BaseModel):
    short: Optional[str]
    target: Optional[str]
    is_private: Optional[bool]
    expiry_period: Optional[int]
    added_at: Optional[dt.datetime]


class UrlDb(Base):
    __tablename__: str = "url"

    short: Mapped[str]
    target: Mapped[str]
    is_private: Mapped[bool]
    expiry_period: Mapped[int]

    added_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.utcnow(),
        server_default=func.now(),
    )

    users: Mapped[list["UserDb"]] = relationship(
        back_populates="urls",
        secondary=UrlUserLinkDb,
    )


@dataclass
class UrlDbList:
    count: int
    data: list[UrlDb]


# Routing schemas


class UrlRouteCreate(BaseModel):
    target: str
    is_private: bool
    expiry_period: int


class UrlRouteRetrieve(UrlDbRead):
    users: list[uuid.UUID]

    @classmethod
    def parse_url_db(cls, url_db: UrlDb) -> "UrlRouteRetrieve":
        url_db_dict = url_db.__dict__
        url_db_dict["users"] = [user.id for user in url_db.users]
        url_route_retrieve = cls.parse_obj(url_db_dict)

        return url_route_retrieve


class UrlRouteList(BaseModel):
    count: int
    data: list[UrlRouteRetrieve]

    @classmethod
    def parse_url_db_list(cls, url_db_list: UrlDbList):
        return cls(
            count=url_db_list.count,
            data=[UrlRouteRetrieve.parse_url_db(url_db) for url_db in url_db_list.data],
        )

    # class Config:
    #     orm_mode = True


class UrlRouteUpdate(BaseModel):
    is_private: Optional[bool]
    expiry_period: Optional[int]
