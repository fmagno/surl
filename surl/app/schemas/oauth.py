import uuid
from pydantic import BaseModel


class State(BaseModel):
    user_id: uuid.UUID
