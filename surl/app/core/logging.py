import logging

from rich.logging import RichHandler
from rich.traceback import install


def setup_logger() -> None:
    setup_root_logger()
    setup_uvicorn_logger()
    setup_sqlalchemy_logger()


def setup_root_logger() -> None:
    logging.basicConfig(
        encoding="utf-8",
        level=logging.NOTSET,
        format="[%(name)s %(thread)s] - %(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    install(show_locals=True)


def setup_uvicorn_logger() -> None:
    uvicorn_access_logger: logging.Logger = logging.getLogger("uvicorn")
    uvicorn_access_logger.handlers = [RichHandler(rich_tracebacks=True)]
    uvicorn_access_logger.propagate = False

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = [RichHandler(rich_tracebacks=True)]
    uvicorn_access_logger.propagate = False

    uvicorn_error_logger: logging.Logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers = [RichHandler(rich_tracebacks=True)]
    uvicorn_error_logger.propagate = False


def setup_sqlalchemy_logger() -> None:
    sqlalchemy_logger: logging.Logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.handlers = [RichHandler(rich_tracebacks=True)]
    sqlalchemy_logger.propagate = False
    sqlalchemy_logger.setLevel(logging.INFO)
