"""Service layer for CostItem CRUD operations and cost aggregation."""

from sqlmodel import select
from database.connection import get_session
from models.cost_item import CostItem


def create_cost_item(cost_item: CostItem) -> CostItem:
    """Saves a new hardware or external cost item to the database."""
    with get_session() as session:
        session.add(cost_item)
        session.commit()
        session.refresh(cost_item)
        return cost_item


def get_all_cost_items() -> list[CostItem]:
    """Returns all cost items from the database."""
    with get_session() as session:
        statement = select(CostItem)
        return session.exec(statement).all()


def get_cost_items_by_topic(topic_id: int) -> list[CostItem]:
    """Returns all cost items for a given topic/project."""
    with get_session() as session:
        statement = select(CostItem).where(CostItem.topic_id == topic_id)
        return session.exec(statement).all()


def update_cost_item(cost_item_id: int, updated_data: dict) -> CostItem:
    """Updates an existing cost item's fields."""
    with get_session() as session:
        statement = select(CostItem).where(CostItem.id == cost_item_id)
        cost_item = session.exec(statement).first()

        if not cost_item:
            raise ValueError(f"CostItem with ID {cost_item_id} not found.")

        # Dynamically update fields based on the dictionary passed in
        for key, value in updated_data.items():
            if hasattr(cost_item, key):
                setattr(cost_item, key, value)

        session.add(cost_item)
        session.commit()
        session.refresh(cost_item)
        return cost_item


def delete_cost_item(cost_item_id: int) -> None:
    """Deletes a cost item from the database."""
    with get_session() as session:
        statement = select(CostItem).where(CostItem.id == cost_item_id)
        cost_item = session.exec(statement).first()

        if cost_item:
            session.delete(cost_item)
            session.commit()