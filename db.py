# db.py: opens garden.db, baking a fresh one from the migrations if it's missing
import sqlite3
from pathlib import Path

from rebuild import rebuild

DB = Path("garden.db")


def connect():
    # Build the database the first time (or after a restart wipes it)
    if not DB.exists():
        rebuild(DB)
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def reset():
    DB.unlink(missing_ok=True)
