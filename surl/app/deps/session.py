from typing import Optional

from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_session import crud_session
from app.db.session import get_db
from app.schemas.session import SessionDb, SessionDbCreate, SessionDbRead
from app.services.session import SessionService, create_session_service


async def create_session(
    db: AsyncSession,
    request: Request,
) -> SessionDb:
    session_db: SessionDb = await crud_session.create(
        db=db,
        obj_in=SessionDbCreate(),
        # commit=True,
        # refresh=True,
    )
    request.session["surl_session"] = str(session_db.id)
    return session_db


async def get_session_service(
    *,
    db: AsyncSession = Depends(get_db),
    request: Request,
    response: Response,
) -> SessionService:
    session_svc: SessionService = await create_session_service(
        db=db,
        request=request,
        response=response,
    )
    return session_svc


async def get_or_create_session(
    *,
    session_svc: SessionService = Depends(get_session_service),
) -> SessionDbRead:
    session: SessionDbRead = await session_svc.get_or_create_session()
    return session
