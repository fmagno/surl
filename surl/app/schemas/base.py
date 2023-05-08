import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Column, DateTime, Field, SQLModel, func, text


class Base(SQLModel):
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    )
    id: uuid.UUID = Field(
        # default_factory=uuid.uuid4,
        # index=True,
        # nullable=False,
        # unique=True,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
