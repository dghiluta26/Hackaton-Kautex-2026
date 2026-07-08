"""Authentication service: password hashing, registration, and login.

Unlike the other service files, this one is fully implemented since
login/registration is the feature being built right now.
"""

import bcrypt
from sqlmodel import select

from database.connection import get_session
from models.user import User, UserRole


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def get_user_by_username(username: str) -> User | None:
    with get_session() as session:
        return session.exec(select(User).where(User.username == username)).first()


def register_user(username: str, password: str, role: UserRole = UserRole.EMPLOYEE) -> User:
    """Create a new user account. Raises ValueError if the username is taken."""
    username = username.strip()
    if not username or not password:
        raise ValueError("Username and password are required.")

    with get_session() as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            raise ValueError(f"Username '{username}' is already taken.")

        user = User(username=username, password_hash=hash_password(password), role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def authenticate_user(username: str, password: str) -> User | None:
    """Return the User if credentials are valid, otherwise None."""
    user = get_user_by_username(username.strip())
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
