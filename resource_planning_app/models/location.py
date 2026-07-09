"""Location model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Location(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: Optional[str] = None
    description: Optional[str] = None
