import logging
from pprint import pformat

import uvicorn
from fastapi import FastAPI, status
from fastapi_utils.timing import add_timing_middleware

# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from starlette.middleware.cors import CORSMiddleware

from app.core import config
from app.core.exceptions import (
    HTTP400BadRequestException,
    HTTP401UnauthorizedException,
    HTTP403ForbiddenException,
    HTTP404NotFoundException,
    HTTP409ConflictException,
    http_400_bad_request_exception_handler,
    http_401_unauthorized_exception_handler,
    http_403_forbidden_exception_handler,
    http_404_notfound_exception_handler,
    http_409_conflict_exception_handler,
)
from app.core.logging import setup_logger
from app.db.sanity import check_db_is_ready
from app.db.session import close_engine
from app.routes.v1 import router_v1

logger = logging.getLogger(__name__)
settings = config.get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url=f"/api/openapi.json",
)

# FastAPIInstrumentor.instrument_app(app)  # experimental
add_timing_middleware(app, record=logger.debug, prefix="profile")

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# setup logging
@app.on_event("startup")
async def startup_event() -> None:
    setup_logger()
    root_logger: logging.Logger = logging.getLogger()
    root_logger.debug("======== Logging setup! ========")
    if settings.DEBUG:
        root_logger.info(pformat(settings.dict()))

    await check_db_is_ready()


@app.on_event("shutdown")
async def shutdown_event():
    root_logger = logging.getLogger()
    root_logger.debug("Disposing db engine...")
    await close_engine()
    root_logger.debug("======== Terminated! ========")


app.add_exception_handler(
    HTTP400BadRequestException,
    http_400_bad_request_exception_handler,
)
app.add_exception_handler(
    HTTP401UnauthorizedException,
    http_401_unauthorized_exception_handler,
)
app.add_exception_handler(
    HTTP403ForbiddenException,
    http_403_forbidden_exception_handler,
)
app.add_exception_handler(
    HTTP404NotFoundException,
    http_404_notfound_exception_handler,
)
app.add_exception_handler(
    HTTP409ConflictException,
    http_409_conflict_exception_handler,
)


@app.get("/", status_code=status.HTTP_200_OK, tags=["health-check"])
async def health_check():
    return ""


app.include_router(router_v1, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(
        settings.API_APP,
        host="0.0.0.0",
        reload=True,
        port=settings.PORT,
        # log_config=uvicorn_log_config,
    )
