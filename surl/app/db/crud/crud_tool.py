import logging

import uuid
from logging import Logger
from typing import Optional, Union

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.db.crud.crud_base import CRUDBase
from app.schemas.employee import EmployeeDb
from app.schemas.shop import ShopDb
from app.schemas.tool import ToolDb, ToolDbCreate, ToolDbUpdate

logger: Logger = logging.getLogger(__name__)


class CRUDTool(CRUDBase[ToolDb, ToolDbCreate, ToolDbUpdate]):
    async def get_multi_by_shop_id(
        self,
        db: AsyncSession,
        shop_id: Union[uuid.UUID, str],
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> list[ToolDb]:
        statement = (
            select(ToolDb)
            .options(joinedload(ToolDb.shop, innerjoin=True))
            .where(ToolDb.shop_id == shop_id)
        )
        if skip:
            statement.offset(skip)
        if limit:
            statement.limit(limit)

        result = await db.execute(statement)
        entries = result.scalars().unique().all()
        return list(entries)

    async def get_multi_by_employee_id(
        self,
        db: AsyncSession,
        employee_id: Union[uuid.UUID, str],
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> list[ToolDb]:
        # select(ToolDb)
        #     .options(joinedload(ToolDb.shop, innerjoin=True))
        #     .where(ToolDb.shop_id == shop_id)

        # statement = (
        #     # select(ToolDb, ShopDb, EmployeeDb)
        #     select([func.avg(ToolDb.weight)])
        #     .options(joinedload(ToolDb.shop, innerjoin=True))
        #     .options(joinedload(ShopDb.employees, innerjoin=True))
        #     .where(EmployeeDb.id == employee_id)
        # )

        statement = func.avg(ToolDb.weight).scalar()

        # statement = (
        #     select(ToolDb)
        #     .join(ToolDb.shop)
        #     .join(ShopDb.employees)
        #     .where(EmployeeDb.id == employee_id)
        # )
        if skip:
            statement.offset(skip)
        if limit:
            statement.limit(limit)

        result = await db.execute(statement)
        # entries = result.scalars().all()
        entries = result.unique().all()
        # entries = result.scalars().unique().all()
        return entries

    async def get_multi_by_employee_name(
        self,
        db: AsyncSession,
        employee_name: str,
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> list[ToolDb]:
        statement = (
            select(ToolDb)
            .join(ToolDb.shop)
            .join(ShopDb.employees)
            .where(EmployeeDb.name == employee_name)
        )
        if skip:
            statement.offset(skip)
        if limit:
            statement.limit(limit)

        result = await db.execute(statement)
        entries = result.scalars().all()
        return list(entries)


crud_tool = CRUDTool(ToolDb)
