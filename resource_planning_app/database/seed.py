"""Seed the database with an initial admin account for testing.

Usage:
    python -m database.seed

Safe to run multiple times: it only creates the admin account if a user
with that username doesn't already exist.
"""

from database.connection import create_db_and_tables
from models.user import UserRole
from services.auth_service import get_user_by_username, register_user

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "Admin123!"


def seed_admin() -> None:
    create_db_and_tables()

    if get_user_by_username(DEFAULT_ADMIN_USERNAME) is not None:
        print(f"Admin user '{DEFAULT_ADMIN_USERNAME}' already exists, skipping.")
        return

    register_user(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, role=UserRole.ADMIN)
    print(f"Seeded admin user -> username: '{DEFAULT_ADMIN_USERNAME}', password: '{DEFAULT_ADMIN_PASSWORD}'")
    print("Change this password before using the app outside of local testing.")


if __name__ == "__main__":
    seed_admin()
