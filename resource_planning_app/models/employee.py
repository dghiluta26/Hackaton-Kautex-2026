from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Employee(SQLModel, table=True):
    """Employee model for tracking headcount and hourly rates."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str
    available_hours_per_year: int = Field(default=1600)
    hourly_rate: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    allocations: List["Allocation"] = Relationship(back_populates="employee")
