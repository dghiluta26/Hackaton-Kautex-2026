"""Service layer for Employee CRUD operations.

This module will contain the functions used by the Employees page to talk
to the database. For now it only holds placeholders.
"""

from database.connection import get_session
from models.employee import Employee


def create_employee(employee: Employee) -> Employee:
    # TODO: add the employee to the database and return the created record
    raise NotImplementedError


def get_all_employees() -> list[Employee]:
    # TODO: return all employees from the database
    raise NotImplementedError


def get_employee_by_id(employee_id: int) -> Employee | None:
    # TODO: return a single employee by id, or None if not found
    raise NotImplementedError


def update_employee(employee_id: int, updated_data: dict) -> Employee:
    # TODO: update an existing employee's fields
    raise NotImplementedError


def delete_employee(employee_id: int) -> None:
    # TODO: delete an employee from the database
    raise NotImplementedError
