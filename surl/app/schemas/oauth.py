from pydantic import BaseModel


class State(BaseModel):
    next: str
    salt: str
