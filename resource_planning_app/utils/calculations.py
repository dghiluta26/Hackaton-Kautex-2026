from typing import List, Dict, Tuple
from sqlmodel import Session, select
from models.employee import Employee
from models.allocation import Allocation
from models.cost_item import CostItem
from models.topic import Topic

class AllocationValidator:
    """Validates the strict 100% capacity rule."""
    
    @staticmethod
    def validate_employee_allocation(session: Session, employee_id: int, exclude_allocation_id: int = None) -> Tuple[bool, float, str]:
        """
        Validate that an employee's total allocation equals 100%.
        
        Args:
            session: Database session
            employee_id: Employee ID to validate
            exclude_allocation_id: Allocation ID to exclude from calculation (for updates)
        
        Returns:
            (is_valid, total_percentage, error_message)
        """
        stmt = select(Allocation).where(Allocation.employee_id == employee_id)
        allocations = session.exec(stmt).all()
        
        total = sum(a.allocation_percentage for a in allocations 
                   if exclude_allocation_id is None or a.id != exclude_allocation_id)
        
        if total < 1.0:
            return False, total, f"Employee allocation is {total*100:.1f}% - must be exactly 100%"
        elif total > 1.0:
            return False, total, f"Employee allocation is {total*100:.1f}% - cannot exceed 100%"
        else:
            return True, total, ""

class HoursCalculator:
    """Calculates allocated hours and costs."""
    
    @staticmethod
    def calculate_allocated_hours(available_hours: int, allocation_percentage: float) -> float:
        """
        Calculate allocated hours from percentage allocation.
        
        Formula: Allocated Hours = available_hours_per_year * allocation_percentage
        """
        return available_hours * allocation_percentage
    
    @staticmethod
    def calculate_hourly_cost(allocated_hours: float, hourly_rate: float) -> float:
        """Calculate cost from allocated hours and hourly rate."""
        return allocated_hours * hourly_rate

class CostCalculator:
    """Calculates topic-level and global costs."""
    
    @staticmethod
    def get_topic_internal_cost(session: Session, topic_id: int) -> float:
        """
        Calculate total internal personnel cost for a topic.
        
        Formula: sum(allocated_hours * hourly_rate) for all employees allocated to topic
        """
        stmt = select(Allocation, Employee).where(
            (Allocation.topic_id == topic_id) &
            (Allocation.employee_id == Employee.id)
        )
        results = session.exec(stmt).all()
        
        total_cost = 0.0
        for allocation, employee in results:
            allocated_hours = HoursCalculator.calculate_allocated_hours(
                employee.available_hours_per_year,
                allocation.allocation_percentage
            )
            total_cost += HoursCalculator.calculate_hourly_cost(allocated_hours, employee.hourly_rate)
        
        return total_cost
    
    @staticmethod
    def get_external_costs_by_type(session: Session, topic_id: int, cost_type: str) -> float:
        """Get sum of external costs for a specific type."""
        stmt = select(CostItem).where(
            (CostItem.topic_id == topic_id) &
            (CostItem.cost_type == cost_type)
        )
        items = session.exec(stmt).all()
        return sum(item.amount for item in items)
    
    @staticmethod
    def get_topic_total_cost(session: Session, topic_id: int) -> Dict[str, float]:
        """
        Calculate complete cost breakdown for a topic.
        
        Formula: Total Cost = Internal Personnel + External Tooling + Testing - Recovery
        """
        internal_cost = CostCalculator.get_topic_internal_cost(session, topic_id)
        external_tooling = CostCalculator.get_external_costs_by_type(session, topic_id, "External Tooling")
        testing = CostCalculator.get_external_costs_by_type(session, topic_id, "Testing")
        recovery = CostCalculator.get_external_costs_by_type(session, topic_id, "Recovery")  # Usually negative
        
        total_cost = internal_cost + external_tooling + testing + recovery
        
        return {
            "internal_personnel": internal_cost,
            "external_tooling": external_tooling,
            "testing": testing,
            "recovery": recovery,
            "total": total_cost
        }
    
    @staticmethod
    def get_global_totals(session: Session) -> Dict[str, float]:
        """Calculate global cost and headcount metrics."""
        stmt = select(Topic)
        topics = session.exec(stmt).all()
        
        total_cost = 0.0
        total_headcount = 0
        
        for topic in topics:
            cost_breakdown = CostCalculator.get_topic_total_cost(session, topic.id)
            total_cost += cost_breakdown["total"]
        
        # Count unique employees with allocations
        stmt_employees = select(Allocation.employee_id).distinct()
        employee_ids = session.exec(stmt_employees).all()
        total_headcount = len(set(employee_ids))
        
        return {
            "total_cost": total_cost,
            "total_headcount": total_headcount,
            "average_cost_per_employee": total_cost / total_headcount if total_headcount > 0 else 0
        }

class ReportGenerator:
    """Generates executive reports and flags."""
    
    @staticmethod
    def get_high_cost_topics(session: Session, threshold_percentage: float = 0.3) -> List[Dict]:
        """
        Flag topics with high external costs relative to total cost.
        
        Args:
            threshold_percentage: Flag if external costs exceed this % of total
        """
        stmt = select(Topic)
        topics = session.exec(stmt).all()
        
        high_cost_topics = []
        total_global_cost = CostCalculator.get_global_totals(session)["total_cost"]
        
        for topic in topics:
            cost_breakdown = CostCalculator.get_topic_total_cost(session, topic.id)
            external_total = (cost_breakdown["external_tooling"] + 
                            cost_breakdown["testing"] + 
                            cost_breakdown["recovery"])
            
            if cost_breakdown["total"] > 0:
                external_ratio = external_total / cost_breakdown["total"]
            else:
                external_ratio = 0
            
            if external_ratio > threshold_percentage:
                high_cost_topics.append({
                    "name": topic.name,
                    "category": topic.category,
                    "business_justification": topic.business_justification,
                    "total_cost": cost_breakdown["total"],
                    "external_cost": external_total,
                    "external_ratio": external_ratio,
                    "cost_breakdown": cost_breakdown
                })
        
        return sorted(high_cost_topics, key=lambda x: x["external_ratio"], reverse=True)
