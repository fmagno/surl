from fastapi import Response, Depends
from fastapi import APIRouter, status

from app.services.session import get_or_create_session


session_router = APIRouter()


@session_router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def use(
    session=Depends(get_or_create_session),
) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
