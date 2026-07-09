"""Service layer for Employee CRUD operations.

This module will contain the functions used by the Employees page to talk
to the database. For now it only holds placeholders.
"""
from sqlmodel import select, Session
from database.connection import get_session
from models.employee import Employee
from models.allocation import Allocation  # Cleanly imported to resolve constraints

def create_employee(employee: Employee, engine=None) -> Employee:
    # Use context manager: if an explicit engine is passed, create an ad-hoc session
    context = Session(engine) if engine else get_session()
    with context as session:
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


def get_all_employees(engine=None) -> list[Employee]:
    context = Session(engine) if engine else get_session()
    with context as session:
        # This grabs every employee from the database
        statement = select(Employee)
        return session.exec(statement).all()


def get_employee_by_id(employee_id: int, engine=None) -> Employee | None:
    context = Session(engine) if engine else get_session()
    with context as session:
        return session.get(Employee, employee_id)


def update_employee(employee_id: int, updated_data: dict, engine=None) -> Employee | None:
    context = Session(engine) if engine else get_session()
    with context as session:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return None
        for key, value in updated_data.items():
            setattr(employee, key, value)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


def delete_employee(employee_id: int, engine=None) -> None:
    context = Session(engine) if engine else get_session()
    with context as session:
        # 1. Safely remove dependent rows from the allocation table first
        allocations_statement = select(Allocation).where(Allocation.employee_id == employee_id)
        allocations = session.exec(allocations_statement).all()
        for allocation in allocations:
            session.delete(allocation)

        # 2. Safely extract and delete the core employee file record
        employee = session.get(Employee, employee_id)
        if employee is not None:
            session.delete(employee)
            session.commit()