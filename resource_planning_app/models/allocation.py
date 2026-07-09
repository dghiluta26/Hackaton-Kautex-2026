from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Allocation(SQLModel, table=True):
    """Allocation model mapping employees to topics with capacity allocation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    topic_id: int = Field(foreign_key="topic.id", index=True)
    allocation_percentage: float  # e.g., 0.40 for 40%
    comment: str = Field(default="")  # Why is this person here?
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    employee: Optional["Employee"] = Relationship(back_populates="allocations")
    topic: Optional["Topic"] = Relationship(back_populates="allocations")
