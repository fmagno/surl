import asyncio
import random
from typing import List

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_employee import crud_employee
from app.db.crud.crud_shop import crud_shop
from app.db.crud.crud_tool import crud_tool
from app.db.session import async_session_factory
from app.schemas.employee import EmployeeDb, EmployeeDbCreate
from app.schemas.shop import ShopDb, ShopDbCreate
from app.schemas.tool import ToolDbCreate

SEED = 0

random.seed(SEED)
fake = Faker()
Faker.seed(SEED)


PERCENTAGE_OF_EMPLOYEES_PER_SHOP = 0.3
PERCENTAGE_OF_TOOLS_PER_SHOP = 0.3
# NUM_EMPLOYEES = 500_000
NUM_EMPLOYEES = 1000
NUM_SHOPS = 10
NUM_TOOLS = 20


async def seed(db: AsyncSession) -> None:
    employees: List[EmployeeDb] = await crud_employee.create_multi(
        db,
        (
            EmployeeDbCreate(name=fake.name(), title=fake.job())
            for i in range(NUM_EMPLOYEES)
        ),
        flush=False,
    )

    tools = await crud_tool.create_multi(
        db,
        (
            ToolDbCreate(
                name=fake.ean13(), weight=fake.unique.random_int(min=1, max=100)
            )
            for _ in range(NUM_TOOLS)
        ),
        flush=False,
    )

    shops: list[ShopDb] = await crud_shop.create_multi_with_employees_and_tools(
        db,
        objs_in=(
            ShopDbCreate(name=fake.company(), location=fake.city())
            for _ in range(NUM_SHOPS)
        ),
        employees=(
            random.sample(
                employees, k=round(NUM_EMPLOYEES * PERCENTAGE_OF_EMPLOYEES_PER_SHOP)
            )
            for _ in range(NUM_SHOPS)
        ),
        tools=(
            random.sample(tools, k=round(NUM_TOOLS * PERCENTAGE_OF_TOOLS_PER_SHOP))
            for _ in range(NUM_SHOPS)
        ),
        commit=True,
    )


# print(f"{shops=}")


async def main() -> None:
    async with async_session_factory() as db:
        await seed(db)


if __name__ == "__main__":
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # ret = loop.run_until_complete(aio_func(*args, **kwargs))
    # loop.close()

    asyncio.run(main())
