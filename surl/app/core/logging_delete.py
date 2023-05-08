import logging

from rich.logging import RichHandler
from rich.traceback import install


def setup_root_logger():
    logging.basicConfig(
        encoding="utf-8",
        level=logging.NOTSET,
        format="[%(name)s %(thread)s] - %(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    install(show_locals=True)


def setup_uvicorn_logger():
    uvicorn_access_logger = logging.getLogger("uvicorn")
    uvicorn_access_logger.handlers = []

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = []
    uvicorn_access_logger.propagate = True

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers = []
    uvicorn_error_logger.propagate = True
