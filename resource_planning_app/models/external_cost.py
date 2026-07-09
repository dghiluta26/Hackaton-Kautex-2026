from sqlmodel import SQLModel, Field
from typing import Optional

class ExternalCost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topic.id") # Links directly to your existing Topics
    item_name: str
    description: Optional[str] = None
    cost: float