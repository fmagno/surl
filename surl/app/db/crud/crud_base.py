import asyncio
import logging
import uuid
from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func
from sqlalchemy import delete

from app.schemas.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseModel)

logger: logging.Logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ListSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        list_model: Type[ListSchemaType],
    ) -> None:
        self.model = model
        self.list_model = list_model

    async def get(
        self,
        db: AsyncSession,
        id: Union[uuid.UUID, str],
    ) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        entry = result.scalar_one_or_none()

        return entry

    async def get_multi(
        self,
        db: AsyncSession,
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> ListSchemaType:
        stmt_count = select(func.count()).select_from(self.model)
        result = await db.execute(stmt_count)
        count = result.scalar_one()

        stmt = select(self.model).offset(skip)

        if limit:
            stmt = stmt.limit(limit)
        result = await db.execute(stmt)
        entries = result.scalars().all()
        return self.list_model(data=entries, count=count)

    async def create(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType,
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in.dict())  # type: ignore
        db.add(db_obj)

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await db.refresh(db_obj)

        return db_obj

    async def create_multi(
        self,
        db: AsyncSession,
        objs_in: Iterable[CreateSchemaType],
        flush: bool = True,
        commit: bool = False,
        refresh: bool = False,
    ) -> List[ModelType]:
        db_objs = [self.model(**o.dict()) for o in objs_in]
        db.add_all(db_objs)

        if flush:
            await db.flush()

        if commit:
            await db.commit()

        if refresh and (flush or commit):
            await asyncio.gather(*[db.refresh(o) for o in db_objs])

        return db_objs

    async def create_bulk(
        self,
        db: AsyncSession,
        objs_in: list[CreateSchemaType],
        flush: bool = True,
        commit: bool = False,
    ) -> None:
        await db.execute(insert(self.model), [obj_in.dict() for obj_in in objs_in])
        if flush:
            await db.flush()
        if commit:
            await db.commit()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        flush: bool = True,
        commit: bool = False,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        if flush:
            await db.flush()
        if commit:
            await db.commit()
        return db_obj

    async def delete(
        self, db: AsyncSession, *, id: Union[uuid.UUID, str]
    ) -> Optional[ModelType]:
        obj = await db.get(self.model, id)
        if obj is not None:
            await db.delete(obj)
        return obj

    async def delete_all(self, db: AsyncSession) -> None:
        statement = delete(self.model)
        await db.execute(statement)

    async def get_random(self, db: AsyncSession) -> Optional[ModelType]:
        stmt = select(self.model).order_by(func.random()).limit(1)
        result = await db.execute(stmt)
        entry = result.scalar_one_or_none()
        return entry
