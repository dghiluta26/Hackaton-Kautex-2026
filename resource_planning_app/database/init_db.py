"""Run this script to initialize the SQLite database and create all tables.

Usage:
    python -m database.init_db
"""

# Import models so SQLModel is aware of them before creating tables.
from models.allocation import Allocation  # noqa: F401
from models.cost_item import CostItem  # noqa: F401
from models.department import Department  # noqa: F401
from models.employee import Employee  # noqa: F401
from models.location import Location  # noqa: F401
from models.team import Team  # noqa: F401
from models.topic import Topic  # noqa: F401

from database.connection import create_db_and_tables


def main() -> None:
    create_db_and_tables()
    print("Database initialized successfully at data/planning.db")


if __name__ == "__main__":
    main()
