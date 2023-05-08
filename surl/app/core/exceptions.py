from typing import Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schemas.http_errors import (
    HTTP400BadRequestResponse,
    HTTP401UnauthorizedResponse,
    HTTP403ForbiddenResponse,
    HTTP404NotFoundResponse,
    HTTP409ConflictResponse,
)


class HTTP400BadRequestException(Exception):
    def __init__(
        self,
        response: Optional[HTTP400BadRequestResponse] = HTTP400BadRequestResponse(),
    ):
        self.response = response


class HTTP401UnauthorizedException(Exception):
    def __init__(
        self,
        response: Optional[HTTP401UnauthorizedResponse] = HTTP401UnauthorizedResponse(),
    ):
        self.response = response


class HTTP403ForbiddenException(Exception):
    def __init__(
        self, response: Optional[HTTP403ForbiddenResponse] = HTTP403ForbiddenResponse()
    ):
        self.response = response


class HTTP404NotFoundException(Exception):
    def __init__(
        self, response: Optional[HTTP404NotFoundResponse] = HTTP404NotFoundResponse()
    ):
        self.response = response


class HTTP409ConflictException(Exception):
    def __init__(
        self, response: Optional[HTTP409ConflictResponse] = HTTP409ConflictResponse()
    ):
        self.response = response


async def http_400_bad_request_exception_handler(
    request: Request, exc: HTTP400BadRequestException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )


async def http_401_unauthorized_exception_handler(
    request: Request, exc: HTTP401UnauthorizedException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )


async def http_403_forbidden_exception_handler(
    request: Request, exc: HTTP403ForbiddenException
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )


async def http_404_notfound_exception_handler(
    request: Request, exc: HTTP404NotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )


async def http_409_conflict_exception_handler(
    request: Request, exc: HTTP409ConflictException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )
