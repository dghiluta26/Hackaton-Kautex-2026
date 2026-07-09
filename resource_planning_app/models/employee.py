"""Employee model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Employee(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    available_hours_per_year: Optional[float] = None
    hourly_rate: Optional[float] = None
    status: Optional[str] = None
    manager: Optional[str] = None
    notes: Optional[str] = None
