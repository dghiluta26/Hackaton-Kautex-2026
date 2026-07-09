import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "planning.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Create SQLite engine
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get a database session for dependency injection."""
    with Session(engine) as session:
        yield session
