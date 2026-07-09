"""Database connection setup for the Resource Planning App.

Reads DATABASE_URL from Streamlit secrets (or the environment) so the app
connects to the shared Supabase/Postgres database. There is deliberately no
silent fallback to a local SQLite file: everyone must point at the same
database, and a missing secret should fail loudly rather than quietly
create an empty local database that looks like data loss.
"""

import os
from pathlib import Path

import streamlit as st
from sqlmodel import Session, SQLModel, create_engine

# Project paths (kept for the one-off sqlite -> Supabase migration script)
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

    raise RuntimeError(
        "DATABASE_URL is not set. Add it to resource_planning_app/.streamlit/secrets.toml "
        "(see secrets.toml.example) or set it as an environment variable before running "
        "the app, so you connect to the shared Supabase database instead of a fresh, "
        "empty local one."
    )


DATABASE_URL = _resolve_database_url()

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Supabase's pooler drops idle connections; check aliveness before reuse
    pool_recycle=300,  # and don't hold onto a pooled connection longer than that anyway
)


def get_session() -> Session:
    """Return a new SQLModel session connected to the app database."""
    return Session(engine)


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel models, if they don't exist yet."""
    import models  # noqa: F401  (registers every table with SQLModel's metadata)

    SQLModel.metadata.create_all(engine)
