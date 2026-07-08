"""Service layer for CostItem CRUD operations and cost aggregation.

This module will contain the functions used by the Reports and Allocation
Matrix pages to talk to the database. For now it only holds placeholders.
"""

from database.connection import get_session
from models.cost_item import CostItem


def create_cost_item(cost_item: CostItem) -> CostItem:
    # TODO: add the cost item to the database and return the created record
    raise NotImplementedError


def get_all_cost_items() -> list[CostItem]:
    # TODO: return all cost items from the database
    raise NotImplementedError


def get_cost_items_by_topic(topic_id: int) -> list[CostItem]:
    # TODO: return all cost items for a given topic
    raise NotImplementedError


def update_cost_item(cost_item_id: int, updated_data: dict) -> CostItem:
    # TODO: update an existing cost item's fields
    raise NotImplementedError


def delete_cost_item(cost_item_id: int) -> None:
    # TODO: delete a cost item from the database
    raise NotImplementedError
