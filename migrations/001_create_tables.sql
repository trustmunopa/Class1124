-- 001: the two tables
CREATE TABLE bed (
    bed_id   INTEGER PRIMARY KEY,
    crop     TEXT NOT NULL,
    location TEXT
);

CREATE TABLE bed_log (
    log_id   INTEGER PRIMARY KEY,
    bed_id   INTEGER NOT NULL REFERENCES bed(bed_id),
    log_date TEXT,
    status   TEXT
);
