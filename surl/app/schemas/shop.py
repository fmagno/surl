import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import Extra
from sqlmodel import Relationship, SQLModel

from app.schemas.base import Base
from app.schemas.employee_shop import EmployeeShopLinkDb

if TYPE_CHECKING:
    from app.schemas.employee import EmployeeDb
    from app.schemas.tool import ToolDb


class ShopBase(SQLModel):
    name: str
    location: str


class ShopDbRead(ShopBase):
    id: uuid.UUID


class ShopDbCreate(ShopBase, extra=Extra.forbid):
    ...


class ShopDbUpdate(SQLModel):
    name: Optional[str]
    location: Optional[str]


class ShopDb(Base, ShopBase, table=True):
    __tablename__ = "shop"

    employees: List["EmployeeDb"] = Relationship(
        back_populates="shops", link_model=EmployeeShopLinkDb
    )
    tools: List["ToolDb"] = Relationship(back_populates="shop")


# Routes schemas #######################################
