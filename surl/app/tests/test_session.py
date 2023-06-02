from typing import Any, Optional

import pytest
from fastapi import status
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.db.crud.crud_session import crud_session

# from app.schemas.auth import Token, TokenPayload
from app.schemas.session import SessionDb, SessionDbList, SessionHttp


async def test_session_creation(
    async_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test that a new session is created when POSTing to /v1/session"""

    response: Response = await async_client.post("v1/session")
    session_cookie: Optional[str] = response.cookies.get("session")
    first_session_db = await crud_session.get_first(db=db_session)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert session_cookie
    assert first_session_db


async def test_session_subsequent_creation(
    async_client: AsyncClient,
    create_session: SessionHttp,
    db_session: AsyncSession,
) -> None:
    """Test that subsequent POSTs to /v1/session won't create new sessions"""

    # response: Response = \
    await async_client.post(
        "v1/session",
        cookies={
            "session": create_session.cookie,
        },
    )
    # session_cookie: Optional[str] = response.cookies.get("session")
    sessions_db: SessionDbList = await crud_session.get_multi(db=db_session)

    assert sessions_db.count == 1
    # assert session_cookie == create_session.cookie
