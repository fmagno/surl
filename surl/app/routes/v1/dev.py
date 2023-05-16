import logging
from typing import Any

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings

# from app.core.exceptions import HTTP400BadRequestException
from app.db.session import get_db
from app.schemas.http_errors import (  # HTTP400BadRequestResponse,
    HTTP400BadRequestContent,
    HTTP401UnauthorizedContent,
)

dev_router = APIRouter()
settings: Settings = get_settings()
logger: logging.Logger = logging.getLogger(__name__)


class HTTP401DevContent(HTTP401UnauthorizedContent):
    code: str = "DEV_01"
    msg: str = "Not authenticated with third party"


class HTTP400DevContent(HTTP400BadRequestContent):
    code: str = "DEV_02"
    msg: str = "Dev 02 error"
    data: dict[str, Any] = {"k1": "v1", "k2": "v2"}


@dev_router.post(
    "/dev1",
    response_model=str,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTP401DevContent,
            "description": "Error raised when request is not authenticated",
        },
    },
    include_in_schema=settings.DEBUG,
)
async def dev1(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> str:
    """Dev 1 endpoint."""

    print("asd")

    return "Done!"
