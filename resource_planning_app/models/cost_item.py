"""CostItem model: extra costs associated with a topic (non-employee costs)."""

from typing import Optional

from sqlmodel import Field, SQLModel


class CostItem(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")
    cost_type: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
