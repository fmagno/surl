from pydantic import BaseModel
import uuid
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

from app.schemas.base import Base


if TYPE_CHECKING:
    from app.schemas.user import UserDb


class SessionBase(BaseModel):
    ...


class SessionDbRead(SessionBase):
    ...


class SessionDbCreate(SessionBase):
    ...


class SessionDbUpdate(SessionBase):
    ...


class SessionDbList(BaseModel):
    count: int
    data: list[SessionDbRead]


class SessionDb(Base, table=True):
    __tablename__ = "session"

    user: "UserDb" = Relationship(back_populates="sessions")
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")
