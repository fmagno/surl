import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.services.base import BaseService

settings: Settings = get_settings()
logger: logging.Logger = logging.getLogger(__name__)


class UserService(BaseService):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db=db)


# Facade #############################


async def create_service(db: AsyncSession) -> UserService:
    user_svc = UserService(db)
    return user_svc
