import datetime as dt
import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.user import UserDb


class SessionBase(BaseModel):
    created_at: dt.datetime


class SessionDbRead(SessionBase):
    id: uuid.UUID


class SessionDbCreate(SessionBase):
    created_at: dt.datetime = dt.datetime.now()


class SessionDbUpdate(BaseModel):
    ...


class SessionDbList(BaseModel):
    count: int
    data: list[SessionDbRead]


class SessionDb(Base, table=True):
    __tablename__ = "session"

    user: "UserDb" = Relationship(back_populates="sessions")
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")


class SessionHttp(BaseModel):
    session: SessionDbRead
    cookie: str
