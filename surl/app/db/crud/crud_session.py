import logging
from logging import Logger

from app.db.crud.crud_base import CRUDBase
from app.schemas.session import (
    SessionDb,
    SessionDbCreate,
    SessionDbList,
    SessionDbUpdate,
)

logger: Logger = logging.getLogger(__name__)


class CRUDSession(
    CRUDBase[
        SessionDb,
        SessionDbCreate,
        SessionDbUpdate,
        SessionDbList,
    ]
):
    ...


crud_session = CRUDSession(
    SessionDb,
    SessionDbList,
)
