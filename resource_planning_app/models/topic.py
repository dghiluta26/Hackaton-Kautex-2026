"""Topic (project) model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Topic(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: Optional[str] = None
    area: Optional[str] = None
    description: Optional[str] = None
    objective: Optional[str] = None
    deliverables: Optional[str] = None
    business_justification: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
