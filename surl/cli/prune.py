from app.db.crud.crud_employee import crud_employee
from app.db.crud.crud_employee_shop import crud_employee_shop
from app.db.crud.crud_shop import crud_shop
from app.db.crud.crud_tool import crud_tool
from app.db.session import async_session_factory


async def prune_aio() -> None:
    print("Deleting all tables...")
    async with async_session_factory() as db:
        await crud_tool.delete_all(db)
        await crud_employee_shop.delete_all(db)
        await crud_employee.delete_all(db)
        await crud_shop.delete_all(db)

        await db.commit()
