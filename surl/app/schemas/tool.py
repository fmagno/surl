import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import Extra
from sqlmodel import Field, Relationship, SQLModel

from app.schemas.base import Base

# from app.schemas.shop import ShopDb

if TYPE_CHECKING:
    from app.schemas.shop import ShopDb

# from app.schemas.visualization import VisualizationDb


class ToolBase(SQLModel):
    name: str
    weight: float


class ToolDbRead(ToolBase):
    id: uuid.UUID


class ToolDbCreate(ToolBase, extra=Extra.forbid):
    ...


class ToolDbUpdate(SQLModel):
    name: Optional[str]
    weight: Optional[float]


class ToolDb(Base, ToolBase, table=True):
    __tablename__ = "tool"

    shop: "ShopDb" = Relationship(back_populates="tools")
    shop_id: uuid.UUID = Field(default=None, foreign_key="shop.id")
