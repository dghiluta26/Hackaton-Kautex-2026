"""Service layer for Allocation CRUD operations.

This module will contain the functions used by the Allocation Matrix page
to talk to the database. For now it only holds placeholders.
"""

from database.connection import get_session
from models.allocation import Allocation


def create_allocation(allocation: Allocation) -> Allocation:
    # TODO: add the allocation to the database and return the created record
    raise NotImplementedError


def get_all_allocations() -> list[Allocation]:
    # TODO: return all allocations from the database
    raise NotImplementedError


def get_allocations_by_employee(employee_id: int) -> list[Allocation]:
    # TODO: return all allocations for a given employee
    raise NotImplementedError


def get_allocations_by_topic(topic_id: int) -> list[Allocation]:
    # TODO: return all allocations for a given topic
    raise NotImplementedError


def update_allocation(allocation_id: int, updated_data: dict) -> Allocation:
    # TODO: update an existing allocation's fields
    raise NotImplementedError


def delete_allocation(allocation_id: int) -> None:
    # TODO: delete an allocation from the database
    raise NotImplementedError
