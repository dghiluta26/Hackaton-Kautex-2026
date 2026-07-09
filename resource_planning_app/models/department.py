"""Department model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Department(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
