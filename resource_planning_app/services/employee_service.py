"""Service layer for Employee CRUD operations.

This module will contain the functions used by the Employees page to talk
to the database. For now it only holds placeholders.
"""
from sqlmodel import select
from database.connection import get_session
from models.employee import Employee

def create_employee(employee: Employee) -> Employee:
    with get_session() as session:
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


def get_all_employees() -> list[Employee]:
    with get_session() as session:
        # This grabs every employee from the database
        statement = select(Employee)
        return session.exec(statement).all()


def get_employee_by_id(employee_id: int) -> Employee | None:
    with get_session() as session:
        return session.get(Employee, employee_id)


def update_employee(employee_id: int, updated_data: dict) -> Employee | None:
    with get_session() as session:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return None
        for key, value in updated_data.items():
            setattr(employee, key, value)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


def delete_employee(employee_id: int) -> None:
    with get_session() as session:
        employee = session.get(Employee, employee_id)
        if employee is not None:
            session.delete(employee)
            session.commit()
