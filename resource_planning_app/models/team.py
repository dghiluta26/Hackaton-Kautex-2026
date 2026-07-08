"""Team model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    description: Optional[str] = None
