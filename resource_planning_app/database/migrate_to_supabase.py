"""One-off migration: copy every row from the local SQLite database into
a Postgres/Supabase database, then fix up the identity sequences so new
inserts don't collide with the copied primary keys.

Usage (run from resource_planning_app/):
    python -m database.migrate_to_supabase "postgresql://...supabase connection string..."

If no connection string is passed as an argument, falls back to the
DATABASE_URL environment variable, then to .streamlit/secrets.toml.
"""

import sys
import tomllib
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from database.connection import DATABASE_PATH

# Tables in FK-safe order: referenced tables before the tables that
# reference them.
TABLE_ORDER = [
    "department",
    "location",
    "team",
    "employee",
    "topic",
    "user",
    "allocation",
    "costitem",
]


def _resolve_target_url() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]

    import os

    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]

    secrets_path = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        with secrets_path.open("rb") as f:
            secrets = tomllib.load(f)
        if "DATABASE_URL" in secrets:
            return secrets["DATABASE_URL"]

    raise SystemExit(
        "No target database URL found. Pass it as an argument, set DATABASE_URL, "
        "or add it to .streamlit/secrets.toml."
    )


def main() -> None:
    target_url = _resolve_target_url()

    if not DATABASE_PATH.exists():
        raise SystemExit(f"No SQLite database found at {DATABASE_PATH}")

    source_engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    target_engine = create_engine(target_url)

    # Make sure the schema exists on the target before copying data.
    import models  # noqa: F401  (registers every table with SQLModel's metadata)
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(target_engine)

    with source_engine.connect() as src_conn, target_engine.begin() as tgt_conn:
        for table in TABLE_ORDER:
            df = pd.read_sql_table(table, src_conn)
            if df.empty:
                print(f"  {table}: 0 rows, skipping")
                continue
            df.to_sql(table, tgt_conn, if_exists="append", index=False)
            print(f"  {table}: copied {len(df)} rows")

            # Realign the Postgres identity sequence so the next auto
            # generated id continues after the highest copied id.
            tgt_conn.execute(
                text(
                    f'SELECT setval(pg_get_serial_sequence(:table, \'id\'), '
                    f'(SELECT COALESCE(MAX(id), 1) FROM "{table}"))'
                ),
                {"table": table},
            )

    print("Migration complete.")


if __name__ == "__main__":
    main()
