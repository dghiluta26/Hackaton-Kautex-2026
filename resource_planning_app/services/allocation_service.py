"""Service layer for Allocation CRUD operations."""

from __future__ import annotations
from sqlmodel import select
from database.connection import get_session
from models.allocation import Allocation

def get_all_allocations() -> list[Allocation]:
    """Fetches all allocations from the database."""
    with get_session() as session:
        statement = select(Allocation)
        return session.exec(statement).all()

def get_allocations_by_employee(employee_id: int) -> list[Allocation]:
    """Fetches every allocation belonging to a single employee."""
    with get_session() as session:
        statement = select(Allocation).where(Allocation.employee_id == employee_id)
        return session.exec(statement).all()

def get_employee_total_allocation(employee_id: int) -> float:
    """Sums an employee's allocation percentage across all topics (0-100 scale)."""
    with get_session() as session:
        statement = select(Allocation).where(Allocation.employee_id == employee_id)
        allocations = session.exec(statement).all()
        return sum(a.allocation_percentage or 0.0 for a in allocations)

def delete_allocation(allocation_id: int) -> None:
    """Removes a single allocation by id."""
    with get_session() as session:
        allocation = session.get(Allocation, allocation_id)
        if allocation is not None:
            session.delete(allocation)
            session.commit()

def upsert_allocation(employee_id: int, topic_id: int, percentage: float, comment: str | None = None) -> None:
    """Updates an existing allocation or creates a new one if it doesn't exist."""
    with get_session() as session:
        # Check if this employee is already assigned to this topic
        statement = select(Allocation).where(
            Allocation.employee_id == employee_id,
            Allocation.topic_id == topic_id
        )
        existing_alloc = session.exec(statement).first()

        if existing_alloc:
            # Update the percentage
            existing_alloc.allocation_percentage = percentage
            if comment is not None:
                existing_alloc.comment = comment
            session.add(existing_alloc)
        else:
            # Create a brand new allocation
            new_alloc = Allocation(
                employee_id=employee_id,
                topic_id=topic_id,
                allocation_percentage=percentage,
                comment=comment
            )
            session.add(new_alloc)

        session.commit()