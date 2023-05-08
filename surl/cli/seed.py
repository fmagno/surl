from app.db.seed import seed
from app.db.session import async_session_factory


async def seed_aio() -> None:
    print("Seeding...")

    async with async_session_factory() as db:
        await seed(db)
