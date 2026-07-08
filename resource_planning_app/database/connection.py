"""Database connection setup for the Resource Planning App.

Creates the SQLite engine used by the whole application and makes sure
the `data/` folder exists before SQLite tries to write the database file.
"""

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "planning.db"

# Make sure the data folder exists before connecting
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# `check_same_thread=False` is needed because Streamlit can access
# the database from different threads.
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def get_session() -> Session:
    """Return a new SQLModel session connected to the app database."""
    return Session(engine)


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel models, if they don't exist yet."""
    import models  # noqa: F401  (registers every table with SQLModel's metadata)

    SQLModel.metadata.create_all(engine)
