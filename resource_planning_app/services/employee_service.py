from sqlmodel import Session, select
from models.employee import Employee
from typing import List, Optional

class EmployeeService:
    """Service for Employee CRUD operations."""
    
    @staticmethod
    def create_employee(session: Session, name: str, location: str, 
                       available_hours_per_year: int = 1600, hourly_rate: float = 0.0) -> Employee:
        """Create a new employee."""
        employee = Employee(
            name=name,
            location=location,
            available_hours_per_year=available_hours_per_year,
            hourly_rate=hourly_rate
        )
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee
    
    @staticmethod
    def get_all_employees(session: Session) -> List[Employee]:
        """Get all employees."""
        stmt = select(Employee).order_by(Employee.name)
        return session.exec(stmt).all()
    
    @staticmethod
    def get_employee_by_id(session: Session, employee_id: int) -> Optional[Employee]:
        """Get employee by ID."""
        return session.get(Employee, employee_id)
    
    @staticmethod
    def update_employee(session: Session, employee_id: int, **kwargs) -> Optional[Employee]:
        """Update employee by ID."""
        employee = session.get(Employee, employee_id)
        if employee:
            for key, value in kwargs.items():
                if hasattr(employee, key):
                    setattr(employee, key, value)
            session.add(employee)
            session.commit()
            session.refresh(employee)
        return employee
    
    @staticmethod
    def delete_employee(session: Session, employee_id: int) -> bool:
        """Delete employee by ID."""
        employee = session.get(Employee, employee_id)
        if employee:
            session.delete(employee)
            session.commit()
            return True
        return False
