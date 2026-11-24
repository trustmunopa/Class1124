-- 002: starting rows (one status is messy on purpose)
INSERT INTO bed VALUES
    (1, 'kale', 'upper garden'),
    (2, 'garlic', 'hoop house'),
    (3, 'tomatoes', 'lower garden');

INSERT INTO bed_log (bed_id, log_date, status) VALUES
    (1, '2026-09-01', 'seeded'),
    (1, '2026-09-20', 'sprouting'),
    (2, '2026-09-05', 'seeded'),
    (2, '2026-09-25', 'Sprouting ');
