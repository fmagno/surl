import logging
import uuid
from logging import Logger
from typing import Any, Optional, Union

# from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.db.crud.crud_base import CRUDBase
from app.schemas.employee import EmployeeDb, EmployeeDbCreate, EmployeeDbUpdate
from app.schemas.employee_shop import EmployeeShopLinkDb
from app.schemas.shop import ShopDb

# from sqlalchemy.sql import select_from


# import uuid
# from typing import Any, List, Optional


logger: Logger = logging.getLogger(__name__)


class CRUDEmployee(CRUDBase[EmployeeDb, EmployeeDbCreate, EmployeeDbUpdate]):
    async def get_multi_by_shop_id(
        self,
        db: AsyncSession,
        shop_id: Union[uuid.UUID, str],
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> list[EmployeeDb]:
        # # SAVE ME

        # statement = (
        #     select(EmployeeShopLinkDb, EmployeeDb, ShopDb)
        #     .join(EmployeeDb)
        #     .join(ShopDb)
        #     .where(ShopDb.id == shop_id)
        # )
        # # statement = statement.join(EmployeeShopLinkDb)
        # result = await db.execute(statement)

        # from rich import print as rprint

        # for employee_shop_link, employee, shop in result:
        #     rprint(f"{employee_shop_link=}\n")
        #     rprint(f"{employee=}\n")
        #     rprint(f"{shop=}\n\n")

        # entries = result.scalars()
        # return list(entries)

        # NEW STUFF
        statement = (
            select(EmployeeDb, ShopDb)
            # .join(EmployeeDb.shops)
            .options(joinedload(EmployeeDb.shops, innerjoin=True)).where(
                ShopDb.id == shop_id
            )
        )
        # statement = statement.join(EmployeeShopLinkDb)
        result = await db.execute(statement)
        entries = result.scalars().unique().all()
        return list(entries)

        # # NEW STUFF 2
        # statement = (
        #     select(EmployeeDb).join(EmployeeDb).join(ShopDb).where(ShopDb.id == shop_id)
        # )
        # # statement = statement.join(EmployeeShopLinkDb)
        # result = await db.execute(statement)

        # from rich import print as rprint

        # for employee in result:
        #     # rprint(f"{employee_shop_link=}\n")
        #     rprint(f"{employee=}\n")
        #     # rprint(f"{shop=}\n\n")

        # entries = result.scalars()
        # return list(entries)

        # OLD STUFF
        #
        # stmt = select(EmployeeDb, EmployeeShopLinkDb, ShopDb)
        # # if skip:
        # #     stmt = stmt.offset(skip)
        # # if limit:
        # #     stmt = stmt.limit(limit)

        # stmt = stmt.where(ShopDb.id == shop_id)
        # result = await db.execute(stmt)
        # entries = result.scalars()
        # return list(entries)

    async def create_with_shops(
        self,
        db: AsyncSession,
        obj_in: EmployeeDbCreate,
        shops: list[ShopDb],
        flush: bool = True,
        commit: bool = False,
    ) -> EmployeeDb:
        # obj_in_data: dict[str, Any] = jsonable_encoder(obj_in)
        obj_in_data: dict[str, Any] = obj_in.dict()
        db_obj = EmployeeDb(**obj_in_data, shops=shops)
        db.add(db_obj)
        if flush:
            await db.flush()
        if commit:
            await db.commit()
        return db_obj

    # async def get_by_upload_id(
    #     self, db: AsyncSession, upload_id: uuid.UUID
    # ) -> Optional[EmployeeDb]:
    #     result = await db.execute(
    #         select(EmployeeDb).where(EmployeeDb.upload_id == upload_id)
    #     )
    #     sample = result.scalars().one_or_none()
    #     return sample

    # async def get_multi_by_upload_id(
    #     self,
    #     db: AsyncSession,
    #     skip: Optional[int] = 0,
    #     limit: Optional[int] = None,
    #     upload_id: Optional[uuid.UUID] = None,
    # ) -> List[EmployeeDb]:
    #     stmt = select(EmployeeDb).offset(skip)
    #     if limit:
    #         stmt = stmt.limit(limit)
    #     if upload_id:
    #         stmt = stmt.where(EmployeeDb.upload_id == upload_id)
    #     result = await db.execute(stmt)
    #     entries = result.scalars()
    #     return list(entries)

    # async def get_multi_by_upload_id_with_relationships(
    #     self,
    #     db: AsyncSession,
    #     skip: Optional[int] = 0,
    #     limit: Optional[int] = None,
    #     upload_id: Optional[uuid.UUID] = None,
    # ) -> List[EmployeeDb]:
    #     stmt = (
    #         select(EmployeeDb)
    #         .offset(skip)
    #         .options(joinedload(EmployeeDb.summary_statistics))
    #         .options(
    #             joinedload(EmployeeDb.visualization).joinedload(VisualizationDb.plots)
    #         )
    #     )
    #     if limit:
    #         stmt = stmt.limit(limit)
    #     if upload_id:
    #         stmt = stmt.where(EmployeeDb.upload_id == upload_id)

    #     result = await db.execute(stmt)
    #     entries = result.scalars().unique().all()
    #     return entries


crud_employee = CRUDEmployee(EmployeeDb)
