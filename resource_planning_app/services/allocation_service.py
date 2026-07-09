from sqlmodel import Session, select
from models.allocation import Allocation
from models.employee import Employee
from models.topic import Topic
from typing import List, Optional, Dict, Tuple

class AllocationService:
    """Service for Allocation CRUD operations."""
    
    @staticmethod
    def create_allocation(session: Session, employee_id: int, topic_id: int, 
                         allocation_percentage: float, comment: str = "") -> Allocation:
        """Create a new allocation."""
        allocation = Allocation(
            employee_id=employee_id,
            topic_id=topic_id,
            allocation_percentage=allocation_percentage,
            comment=comment
        )
        session.add(allocation)
        session.commit()
        session.refresh(allocation)
        return allocation
    
    @staticmethod
    def get_all_allocations(session: Session) -> List[Allocation]:
        """Get all allocations."""
        stmt = select(Allocation)
        return session.exec(stmt).all()
    
    @staticmethod
    def get_allocation_by_id(session: Session, allocation_id: int) -> Optional[Allocation]:
        """Get allocation by ID."""
        return session.get(Allocation, allocation_id)
    
    @staticmethod
    def get_allocations_by_employee(session: Session, employee_id: int) -> List[Allocation]:
        """Get all allocations for an employee."""
        stmt = select(Allocation).where(Allocation.employee_id == employee_id)
        return session.exec(stmt).all()
    
    @staticmethod
    def get_allocations_by_topic(session: Session, topic_id: int) -> List[Allocation]:
        """Get all allocations for a topic."""
        stmt = select(Allocation).where(Allocation.topic_id == topic_id)
        return session.exec(stmt).all()
    
    @staticmethod
    def update_allocation(session: Session, allocation_id: int, **kwargs) -> Optional[Allocation]:
        """Update allocation by ID."""
        allocation = session.get(Allocation, allocation_id)
        if allocation:
            for key, value in kwargs.items():
                if hasattr(allocation, key):
                    setattr(allocation, key, value)
            session.add(allocation)
            session.commit()
            session.refresh(allocation)
        return allocation
    
    @staticmethod
    def delete_allocation(session: Session, allocation_id: int) -> bool:
        """Delete allocation by ID."""
        allocation = session.get(Allocation, allocation_id)
        if allocation:
            session.delete(allocation)
            session.commit()
            return True
        return False
    
    @staticmethod
    def get_employee_total_allocation(session: Session, employee_id: int) -> float:
        """Get total allocation percentage for an employee across all topics."""
        stmt = select(Allocation).where(Allocation.employee_id == employee_id)
        allocations = session.exec(stmt).all()
        return sum(a.allocation_percentage for a in allocations)
    
    @staticmethod
    def get_allocation_matrix(session: Session) -> Dict[int, Dict[int, float]]:
        """
        Get a matrix of employee -> topic allocations.
        Returns: {employee_id: {topic_id: allocation_percentage}}
        """
        stmt = select(Allocation)
        allocations = session.exec(stmt).all()
        
        matrix = {}
        for allocation in allocations:
            if allocation.employee_id not in matrix:
                matrix[allocation.employee_id] = {}
            matrix[allocation.employee_id][allocation.topic_id] = allocation.allocation_percentage
        
        return matrix
