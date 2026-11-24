# rebuild.py: builds a fresh database from raw/ and migrations/
import sqlite3
from pathlib import Path

import pandas as pd

RAW = Path("raw")
MIGRATIONS = Path("migrations")


def rebuild(db_path):
    conn = sqlite3.connect(db_path)

    # 1. Load every CSV in raw/ as its own table: raw/fake_checkins.csv -> raw_fake_checkins
    if RAW.exists():
        for csv in sorted(RAW.glob("*.csv")):
            pd.read_csv(csv).to_sql("raw_" + csv.stem, conn, index=False)
            print("loaded", csv.name)

    # 2. Run every migration, in number order: 001, 002, 003...
    for sql_file in sorted(MIGRATIONS.glob("*.sql")):
        conn.executescript(sql_file.read_text())
        print("ran", sql_file.name)

    conn.commit()
    conn.close()


# Lets us run it by hand too:  python rebuild.py
if __name__ == "__main__":
    Path("garden.db").unlink(missing_ok=True)
    rebuild("garden.db")
