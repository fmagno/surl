from fastapi import APIRouter

# from .auth import auth_router
# from .dev import dev_router
from .user import user_router

router_v1 = APIRouter()
# router_v1.include_router(auth_router, prefix="/auth", tags=["auth"])
# router_v1.include_router(dev_router, prefix="/dev", tags=["dev"])
router_v1.include_router(user_router, prefix="/users", tags=["user"])
