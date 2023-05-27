import asyncio
import datetime as dt
import uuid
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func, select, text
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import joinedload


engine: AsyncEngine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:50432/postgres",
    echo=True,
    future=True,
    pool_size=100,
    max_overflow=100,
)


async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session


class Parent(SQLModel, table=True):
    __tablename__ = "parent"

    id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    name: str

    children: list["Child"] = Relationship(back_populates="parent")


class Child(SQLModel, table=True):
    __tablename__ = "child"

    id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )

    name: str

    parent: "Parent" = Relationship(back_populates="children")
    parent_id: uuid.UUID = Field(default=None, foreign_key="parent.id")


async def create_tables(engine: AsyncEngine):
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def main():
    # await create_tables(engine=engine)
    async with async_session_factory() as db:
        stmt = (
            # select(Parent)
            # .join(Parent.children)
            # .where(Child.id == "6b9ba5fd-6d19-4adb-be8c-b0e07080d714")
            select(Parent)
            .options(joinedload(Parent.children, innerjoin=True))
            .where(Child.id == "2063c4ad-2f62-4416-a057-deee1337467c")
        )

        # stmt = select(UserDb, SessionDb).where(SessionDb.id == session_id)
        result = await db.execute(stmt)
        # entry = result.scalars().one_or_none()
        entry = result.scalars().unique().one_or_none()
        # entry = result.scalar_one_or_none()
        return entry


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
