# queries.py: every SQL statement in the app, one function each.
# Each function takes conn (from db.connect()) first.
import sqlite3

import pandas as pd


# ---------- READ ----------

def crops(conn):
    return pd.read_sql_query("SELECT crop FROM bed ORDER BY crop", conn)["crop"]


def beds(conn):
    return pd.read_sql_query("SELECT crop, location, sun FROM bed ORDER BY crop", conn)


def status_counts(conn):
    return pd.read_sql_query(
        "SELECT status, COUNT(*) AS n FROM bed_log GROUP BY status ORDER BY status", conn
    )


def visits_per_crop(conn):
    # LEFT JOIN so a bed with no visits still shows up with 0
    return pd.read_sql_query(
        """
        SELECT b.crop, COUNT(l.log_id) AS visits
        FROM bed b
        LEFT JOIN bed_log l ON l.bed_id = b.bed_id
        GROUP BY b.crop
        ORDER BY b.crop
        """,
        conn,
    )


def totals(conn):
    # One row with three numbers, for the st.metric tiles on the home page
    return pd.read_sql_query(
        """
        SELECT
            (SELECT COUNT(*) FROM bed)                        AS beds,
            (SELECT COUNT(*) FROM bed_log)                    AS visits,
            (SELECT COUNT(DISTINCT status) FROM bed_log)      AS statuses
        """,
        conn,
    ).iloc[0]


def history(conn, crop):
    return pd.read_sql_query(
        """
        SELECT l.log_date, l.status
        FROM bed_log l
        JOIN bed b ON b.bed_id = l.bed_id
        WHERE b.crop = ?
        ORDER BY l.log_date
        """,
        conn,
        params=(crop,),
    )


def orphan_count(conn):
    return pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM bed_log WHERE bed_id NOT IN (SELECT bed_id FROM bed)",
        conn,
    )["n"][0]


def all_logs(conn):
    return pd.read_sql_query(
        """
        SELECT l.log_id, b.crop, l.log_date, l.status
        FROM bed_log l
        JOIN bed b ON b.bed_id = l.bed_id
        ORDER BY l.log_date
        """,
        conn,
    )


# ---------- CREATE / UPDATE / DELETE ----------

def add_visit(conn, crop, visit_date, status):
    conn.execute(
        "INSERT INTO bed_log (bed_id, log_date, status) "
        "SELECT bed_id, ?, ? FROM bed WHERE crop = ?",
        (str(visit_date), status, crop),
    )
    conn.commit()


def fix_crop(conn, old, new):
    conn.execute("UPDATE bed SET crop = ? WHERE crop = ?", (new, old))
    conn.commit()


def remove_bed(conn, crop):
    # True if the bed was removed, False if it still has logs
    try:
        conn.execute("DELETE FROM bed WHERE crop = ?", (crop,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False


def save_logs(conn, edited):
    # Write every row of the edited table back to bed_log.
    # Returns None if it worked, or the database's error message if it didn't.
    try:
        for row in edited.itertuples():
            conn.execute(
                "UPDATE bed_log SET log_date = ?, status = ? WHERE log_id = ?",
                (row.log_date, row.status, row.log_id),
            )
        conn.commit()
        return None
    except sqlite3.IntegrityError as e:
        conn.rollback()  # all or nothing: undo every row from this save
        return str(e)
