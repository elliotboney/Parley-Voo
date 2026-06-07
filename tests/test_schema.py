"""Smoke test: schema/index.sql creates all 8 spec-locked tables."""

import re
import sqlite3
from pathlib import Path

import pytest

SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "index.sql"

REGULAR_TABLES = {
    "people",
    "conversations",
    "turns",
    "patterns",
    "conflicts",
    "advice_outcomes",
    "meta",
}


def _connect(load_vec: bool) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    if load_vec:
        import sqlite_vec

        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
    return conn


def _vec_available() -> bool:
    conn = sqlite3.connect(":memory:")
    if not hasattr(conn, "enable_load_extension"):
        return False
    try:
        import sqlite_vec  # noqa: F401

        conn.enable_load_extension(True)
        return True
    except (ImportError, AttributeError, sqlite3.OperationalError):
        return False


def test_regular_tables_exist():
    """The 7 plain tables must always be creatable with stdlib sqlite3."""
    # Strip only the vec_turns virtual-table statement (needs the sqlite-vec extension)
    sql = re.sub(
        r"CREATE VIRTUAL TABLE vec_turns.*?;",
        "",
        SCHEMA_PATH.read_text(),
        flags=re.DOTALL,
    )
    conn = _connect(load_vec=False)
    conn.executescript(sql)
    tables = {
        r[0]
        for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    missing = REGULAR_TABLES - tables
    assert not missing, f"schema/index.sql missing tables: {missing}"


def test_vec_turns_table_exists():
    """vec_turns (sqlite-vec vec0 virtual table) — skipped only if the extension can't load."""
    if not _vec_available():
        pytest.skip("sqlite-vec extension unavailable on this interpreter")
    conn = _connect(load_vec=True)
    conn.executescript(SCHEMA_PATH.read_text())
    tables = {
        r[0]
        for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    assert "vec_turns" in tables, "vec_turns virtual table missing from schema"
