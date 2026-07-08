"""Department model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
