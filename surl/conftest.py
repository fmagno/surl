import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.db.session import get_db
from app.main import app
from app.schemas.auth import TokenPayload
from app.core.config import Settings, get_settings

settings: Settings = get_settings()

pytest_plugins: list = [
    # "app.tests.example_module",
]


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    yield "asyncio"


@pytest.fixture()
def base_url() -> str:
    return settings.BASE_URL


@pytest.fixture()
def db_url() -> str:
    return settings.DATABASE_URL


# @pytest.fixture()
# def client_key_secret() -> tuple[str, str]:
#     return (settings.API_CLIENT_KEY, settings.API_CLIENT_SECRET)


# @pytest.fixture()
# def valid_client_token_payload(client_key_secret: tuple[str, str]) -> TokenPayload:
#     client_key, client_secret = client_key_secret
#     return TokenPayload(
#         sub=client_key,
#     )


@pytest.fixture()
async def create_db(
    anyio_backend: str, db_url: str
) -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database and use it for the whole test session."""
    test_engine: AsyncEngine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        # pool_size=100,
        # max_overflow=100,
    )

    # create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # run test
    yield test_engine

    # async with test_engine.begin() as conn:
    #     await conn.run_sync(SQLModel.metadata.drop_all)

    # Drop the entire database
    # drop_database(db_url)


@pytest.fixture
async def db_session(create_db: AsyncEngine):
    """Prepare database session."""

    engine: AsyncEngine = create_db

    async_session_factory = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session_factory() as session:
        # ... setup
        yield session
        # ... teardown
        await session.rollback()


@pytest.fixture
async def async_client(db_session: AsyncSession, base_url: str):
    """Get a TestClient instance that reads/write to the test database."""

    def get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = get_db_override

    async with AsyncClient(app=app, base_url=base_url) as ac:
        yield ac
