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
        import sqlite_vec

        conn.enable_load_extension(True)
        sqlite_vec.load(conn)  # actually attempt the load, not just the import
        return True
    except (ImportError, AttributeError, sqlite3.OperationalError):
        return False
    finally:
        conn.close()


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


def _plain_schema_conn() -> sqlite3.Connection:
    """Connection with all non-vec tables created."""
    sql = re.sub(
        r"CREATE VIRTUAL TABLE vec_turns.*?;",
        "",
        SCHEMA_PATH.read_text(),
        flags=re.DOTALL,
    )
    conn = _connect(load_vec=False)
    conn.executescript(sql)
    return conn


def test_meta_is_single_row():
    """meta must reject a second row (single-row config table)."""
    conn = _plain_schema_conn()
    conn.execute(
        "INSERT INTO meta (embedding_model_id, lexicon_version, schema_version)"
        " VALUES ('m', 'v1', 1)"
    )
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO meta (embedding_model_id, lexicon_version, schema_version)"
            " VALUES ('m2', 'v2', 2)"
        )


def test_participants_must_be_json_array():
    """conversations.participants must be a JSON array of slugs."""
    conn = _plain_schema_conn()
    conn.execute(
        "INSERT INTO conversations (source, occurred_at, setting, participants)"
        " VALUES ('imessage', '2026-06-05T14:30:00Z', '1:1', '[\"me\", \"sam\"]')"
    )
    for bad in ("not json", '"just-a-string"', '{"a": 1}'):
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO conversations (source, occurred_at, setting, participants)"
                " VALUES ('imessage', '2026-06-05T14:30:00Z', '1:1', ?)",
                (bad,),
            )


def test_forecast_prob_bounds():
    """advice_outcomes.forecast_prob must be within [0, 1]."""
    conn = _plain_schema_conn()
    conn.execute(
        "INSERT INTO people (slug, display_name, created_at)"
        " VALUES ('sam', 'Sam', '2026-06-05T14:30:00Z')"
    )
    conn.execute(
        "INSERT INTO advice_outcomes (person_id, seat, forecast_prob, predicted_at)"
        " VALUES (1, 'realist', 0.7, '2026-06-05T14:30:00Z')"
    )
    for bad in (-0.1, 1.5):
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO advice_outcomes (person_id, seat, forecast_prob, predicted_at)"
                " VALUES (1, 'realist', ?, '2026-06-05T14:30:00Z')",
                (bad,),
            )


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
