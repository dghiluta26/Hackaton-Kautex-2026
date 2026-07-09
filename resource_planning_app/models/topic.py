from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Topic(SQLModel, table=True):
    """Topic (Project) model for tracking projects and initiatives."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str  # e.g., "Internal Efforts", "Customer Request", "Allegro", "Pentatonic"
    business_justification: str  # Text block for executive pitching
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    allocations: List["Allocation"] = Relationship(back_populates="topic")
    cost_items: List["CostItem"] = Relationship(back_populates="topic")
