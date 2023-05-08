import uuid
from typing import Optional

from pydantic import Extra
from sqlmodel import Field, SQLModel

from app.schemas.base import Base


class EmployeeShopLinkBase(SQLModel):
    ...


class EmployeeShopLinkDbRead(EmployeeShopLinkBase):
    id: uuid.UUID


class EmployeeShopLinkDbCreate(EmployeeShopLinkBase, extra=Extra.forbid):
    ...


class EmployeeShopLinkDbUpdate(SQLModel):
    ...


class EmployeeShopLinkDb(Base, EmployeeShopLinkBase, table=True):
    __tablename__ = "employee_shop_link"

    shop_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="shop.id", primary_key=True
    )

    employee_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="employee.id", primary_key=True
    )


# Routes schemas #######################################
