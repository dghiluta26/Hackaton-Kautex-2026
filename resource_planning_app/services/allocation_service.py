"""Service layer for Allocation CRUD operations."""

from sqlmodel import select
from database.connection import get_session
from models.allocation import Allocation

def get_all_allocations() -> list[Allocation]:
    """Fetches all allocations from the database."""
    with get_session() as session:
        statement = select(Allocation)
        return session.exec(statement).all()

def upsert_allocation(employee_id: int, topic_id: int, percentage: float) -> None:
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
            session.add(existing_alloc)
        else:
            # Create a brand new allocation
            new_alloc = Allocation(
                employee_id=employee_id,
                topic_id=topic_id,
                allocation_percentage=percentage
            )
            session.add(new_alloc)

        session.commit()

# (Leave the other placeholders below if you want, but we only need these two for the matrix)