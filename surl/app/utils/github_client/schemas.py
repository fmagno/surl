from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    scope: str
    token_type: str
