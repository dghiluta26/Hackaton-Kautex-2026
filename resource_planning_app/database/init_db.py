"""Run this script to initialize the SQLite database and create all tables.

Usage:
    python -m database.init_db
"""

from database.connection import create_db_and_tables


def main() -> None:
    create_db_and_tables()
    print("Database initialized successfully at data/planning.db")


if __name__ == "__main__":
    main()
