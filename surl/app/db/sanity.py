import logging

from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
logger.handlers = []

# try for 4 seconds
max_tries = 4
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.ERROR),
)
async def check_db_is_ready() -> None:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            tables = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )
            logger.debug(f"Database tables: {tables}")
    except OperationalError as e:
        logger.error(f"Failed with sqlalchemy operational error (code: {e})")
        raise e
    except ConnectionRefusedError as e:
        logger.error(f"Failed to connect to database [error: {e}]")
        raise e
    except Exception as e:
        logger.error(f"Failed with an unexpected error: {e}")
        raise
