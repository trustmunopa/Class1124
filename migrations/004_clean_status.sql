-- 004: 'Sprouting ' and 'sprouting' are the same thing. Make them match.
UPDATE bed_log SET status = LOWER(TRIM(status));
