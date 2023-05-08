# import asyncio
import logging
import uuid

# from pprint import pformat
from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.crud.crud_employee import crud_employee

# from app.core.exceptions import HTTP400BadRequestException
from app.db.crud.crud_shop import crud_shop
from app.db.crud.crud_tool import crud_tool
from app.db.session import get_db
from app.schemas.http_errors import (  # HTTP400BadRequestResponse,
    HTTP400BadRequestContent,
    HTTP401UnauthorizedContent,
)
from app.schemas.shop import ShopDbCreate

dev_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


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
    db: AsyncSession = Depends(get_db),
) -> str:
    """Dev 1 endpoint."""

    tools = await crud_tool.get_multi_by_employee_id(
        db,
        employee_id="11a96d65-14cb-4fa1-854c-39cd1b840845",
    )
    # print(f"{tools=}")

    # shop_1 = await crud_shop.create(
    #     db,
    #     ShopDbCreate(
    #         name="continente",
    #         location="Ovar",
    #     ),
    #     flush=True,
    #     commit=False,
    # )

    # shops = await crud_shop.get_multi(db)
    # employees = await crud_employee.get_multi_by_shop_id(db, shops[0].id)

    # print(employees)

    # shops = await crud_shop.get_multi(db)
    # tools = await crud_tool.get_multi_by_shop_id(db, shops[0].id)

    # print(f"{tools=}")

    return "Done!"


# @dev_router.post(
#     "/dev2",
#     response_model=str,
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {
#             "model": HTTP400DevContent,
#             "description": "A bad request error is raised when...",
#         },
#     },
#     include_in_schema=settings.DEBUG,
# )
# async def dev2(
#     db: AsyncSession = Depends(get_db),
# ) -> str:
#     """Dev 2 endpoint."""

#     raise HTTP400BadRequestException(
#         response=HTTP400BadRequestResponse(
#             content=HTTP400DevContent(data={"k55": "v55"})
#         )
#     )


# @dev_router.post(
#     "/dev3",
#     response_model=str,
#     status_code=status.HTTP_200_OK,
#     include_in_schema=settings.DEBUG,
# )
# async def dev3(
#     # db: AsyncSession = Depends(get_db)
# ) -> str:
#     """Dev 3 endpoint."""
#     logger.info(" ======== Dev3 =========")
#     logger.info(" =======================")
#     return "True"
