"""Database connection setup for the Resource Planning App.

Reads DATABASE_URL from Streamlit secrets (or the environment) so the app
can point at Supabase/Postgres. Falls back to a local SQLite file under
`data/` when no DATABASE_URL is configured, which keeps local dev working
without any secrets set up.
"""

import os
from pathlib import Path

import streamlit as st
from sqlmodel import Session, SQLModel, create_engine

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "planning.db"


def _resolve_database_url() -> str:
    try:
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
    except FileNotFoundError:
        pass  # no secrets.toml present, e.g. bare `python` scripts

    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]

    # Local fallback: SQLite file under data/
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{DATABASE_PATH}"


DATABASE_URL = _resolve_database_url()

# `check_same_thread=False` is only needed for SQLite (Streamlit can access
# the database from different threads); Postgres connections don't need it.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def get_session() -> Session:
    """Return a new SQLModel session connected to the app database."""
    return Session(engine)


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel models, if they don't exist yet."""
    import models  # noqa: F401  (registers every table with SQLModel's metadata)

    SQLModel.metadata.create_all(engine)
