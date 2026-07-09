from sqlmodel import Session, select
from models.cost_item import CostItem
from typing import List, Optional

class CostService:
    """Service for CostItem CRUD operations."""
    
    @staticmethod
    def create_cost_item(session: Session, topic_id: int, cost_type: str, 
                        amount: float, description: str = "") -> CostItem:
        """Create a new cost item."""
        cost_item = CostItem(
            topic_id=topic_id,
            cost_type=cost_type,
            amount=amount,
            description=description
        )
        session.add(cost_item)
        session.commit()
        session.refresh(cost_item)
        return cost_item
    
    @staticmethod
    def get_all_cost_items(session: Session) -> List[CostItem]:
        """Get all cost items."""
        stmt = select(CostItem)
        return session.exec(stmt).all()
    
    @staticmethod
    def get_cost_item_by_id(session: Session, cost_item_id: int) -> Optional[CostItem]:
        """Get cost item by ID."""
        return session.get(CostItem, cost_item_id)
    
    @staticmethod
    def get_cost_items_by_topic(session: Session, topic_id: int) -> List[CostItem]:
        """Get all cost items for a topic."""
        stmt = select(CostItem).where(CostItem.topic_id == topic_id).order_by(CostItem.cost_type)
        return session.exec(stmt).all()
    
    @staticmethod
    def get_cost_items_by_type(session: Session, topic_id: int, cost_type: str) -> List[CostItem]:
        """Get cost items of a specific type for a topic."""
        stmt = select(CostItem).where(
            (CostItem.topic_id == topic_id) &
            (CostItem.cost_type == cost_type)
        )
        return session.exec(stmt).all()
    
    @staticmethod
    def update_cost_item(session: Session, cost_item_id: int, **kwargs) -> Optional[CostItem]:
        """Update cost item by ID."""
        cost_item = session.get(CostItem, cost_item_id)
        if cost_item:
            for key, value in kwargs.items():
                if hasattr(cost_item, key):
                    setattr(cost_item, key, value)
            session.add(cost_item)
            session.commit()
            session.refresh(cost_item)
        return cost_item
    
    @staticmethod
    def delete_cost_item(session: Session, cost_item_id: int) -> bool:
        """Delete cost item by ID."""
        cost_item = session.get(CostItem, cost_item_id)
        if cost_item:
            session.delete(cost_item)
            session.commit()
            return True
        return False
