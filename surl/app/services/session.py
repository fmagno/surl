from typing import Optional

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_session import crud_session
from app.schemas.session import SessionDb, SessionDbCreate, SessionDbRead
from app.services.base import BaseService


class SessionService(BaseService):
    def __init__(
        self,
        db: AsyncSession,
        request: Request,
        response: Response,
    ) -> None:
        super().__init__(db=db)
        self.request: Request = request
        self.response: Response = response

    async def create_session(
        self,
    ) -> SessionDb:
        session_db: SessionDb = await crud_session.create(
            db=self.db,
            obj_in=SessionDbCreate(),
        )
        self.request.session["surl_session"] = str(session_db.id)
        return session_db

    async def get_or_create_session(
        self,
    ) -> SessionDbRead:
        if self.request.session:
            session_db: Optional[SessionDb] = await crud_session.get(
                db=self.db,
                id=self.request.session["surl_session"],
            )
            if not session_db:
                self.response.delete_cookie("surl_session")
                session_db = await self.create_session()
        else:
            session_db = await self.create_session()
        session_db_read: SessionDbRead = SessionDbRead.from_orm(session_db)
        return session_db_read


async def create_session_service(
    db: AsyncSession,
    request: Request,
    response: Response,
) -> SessionService:
    session_svc: SessionService = SessionService(
        db=db,
        request=request,
        response=response,
    )
    return session_svc
