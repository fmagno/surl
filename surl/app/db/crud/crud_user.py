import logging
from logging import Logger

from app.db.crud.crud_base import CRUDBase
from app.schemas.user import UserDb, UserDbCreate, UserDbList, UserDbUpdate

logger: Logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[UserDb, UserDbCreate, UserDbUpdate, UserDbList]):
    ...


crud_user = CRUDUser(UserDb, UserDbList)
