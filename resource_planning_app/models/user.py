"""User model: login accounts, separate from Employee (HR) data.

An admin does not need to be an Employee, so auth lives in its own table.
A User can optionally be linked to an Employee record (employee_id) once
that employee is given a login.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.EMPLOYEE)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
