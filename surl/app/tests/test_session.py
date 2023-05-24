from typing import Any, Optional

from app.core import security
from app.schemas.auth import Token, TokenPayload
from fastapi import status
from httpx import AsyncClient, Response


async def test_auth_generate_access_token(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post("v1/session")
    # response_data: Any = response.json()
    # print(response_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT


# async def test_auth_use_access_token(
#     async_client: AsyncClient, valid_client_token_payload: TokenPayload
# ) -> None:
#     jwt_token: str = security.encode_token(valid_client_token_payload)
#     response: Response = await async_client.post(
#         "v1/auth/test-token",
#         headers={"Authorization": f"Bearer {jwt_token}"},
#     )
#     assert response.status_code == status.HTTP_204_NO_CONTENT
