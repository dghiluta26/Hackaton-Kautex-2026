"""Allocation model: links an employee to a topic with a percentage of time."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Allocation(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")
    allocation_percentage: Optional[float] = None
    comment: Optional[str] = None
