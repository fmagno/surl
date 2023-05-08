import asyncio
import logging
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_base import CRUDBase
from app.schemas.employee import EmployeeDb, EmployeeDbCreate
from app.schemas.shop import ShopDb, ShopDbCreate, ShopDbUpdate
from app.schemas.tool import ToolDb

# import uuid
# from typing import Any, List, Optional


logger = logging.getLogger(__name__)


class CRUDShop(CRUDBase[ShopDb, ShopDbCreate, ShopDbUpdate]):
    async def create_with_employees_and_tools(
        self,
        db: AsyncSession,
        obj_in: ShopDbCreate,
        employees: list[EmployeeDb],
        tools: list[ToolDb],
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> ShopDb:
        shop: ShopDb = await self.create(db, obj_in=obj_in, flush=False)
        shop.employees = employees
        shop.tools = tools

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await db.refresh(shop)

        return shop

    async def create_multi_with_employees_and_tools(
        self,
        db: AsyncSession,
        objs_in: Iterable[ShopDbCreate],
        employees: Iterable[list[EmployeeDb]],
        tools: Iterable[list[ToolDb]],
        flush: bool = True,
        commit: bool = False,
        refresh: bool = True,
    ) -> list[ShopDb]:
        shops = await asyncio.gather(
            *[
                self.create_with_employees_and_tools(
                    db,
                    shop,
                    employees=shop_employees,
                    tools=shop_tools,
                    flush=False,
                )
                for (shop, shop_employees, shop_tools) in zip(objs_in, employees, tools)
            ]
        )

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await asyncio.gather(*[db.refresh(o) for o in shops])

        return shops


crud_shop = CRUDShop(ShopDb)
