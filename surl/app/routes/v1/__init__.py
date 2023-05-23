from fastapi import APIRouter

from .auth import auth_router
from .dev import dev_router
from .oauth import oauth_router
from .url import url_router
from .user import user_router
from .session import session_router

router_v1 = APIRouter()
router_v1.include_router(auth_router, prefix="/auth", tags=["auth"])
router_v1.include_router(dev_router, prefix="/dev", tags=["dev"])
router_v1.include_router(user_router, prefix="/users", tags=["user"])
router_v1.include_router(url_router, prefix="/urls", tags=["url"])
router_v1.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
router_v1.include_router(session_router, prefix="/session", tags=["sessions"])
