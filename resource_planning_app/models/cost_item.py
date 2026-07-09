from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class CostItem(SQLModel, table=True):
    """CostItem model for tracking external costs and recovery amounts."""
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topic.id", index=True)
    cost_type: str  # "Internal", "External Tooling", "Testing", "Recovery"
    amount: float  # Negative values for Recovery
    description: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    topic: Optional["Topic"] = Relationship(back_populates="cost_items")
