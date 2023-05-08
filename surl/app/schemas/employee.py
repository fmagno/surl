import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import Extra
from sqlmodel import Field, Relationship, SQLModel

from app.schemas.base import Base
from app.schemas.employee_shop import EmployeeShopLinkDb

if TYPE_CHECKING:
    from app.schemas.shop import ShopDb


class EmployeeBase(SQLModel):
    name: str = Field(index=True)
    title: str


class EmployeeDbRead(EmployeeBase):
    id: uuid.UUID


class EmployeeDbCreate(EmployeeBase, extra=Extra.forbid):
    ...


class EmployeeDbUpdate(SQLModel):
    name: Optional[str]
    title: Optional[str]


class EmployeeDb(Base, EmployeeBase, table=True):
    __tablename__ = "employee"

    shops: List["ShopDb"] = Relationship(
        back_populates="employees", link_model=EmployeeShopLinkDb
    )


# Routes schemas #######################################
