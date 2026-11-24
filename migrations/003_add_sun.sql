-- 003: how much sun each bed gets
ALTER TABLE bed ADD COLUMN sun TEXT;

UPDATE bed SET sun = 'full sun'   WHERE crop = 'tomatoes';
UPDATE bed SET sun = 'part shade' WHERE crop = 'kale';
UPDATE bed SET sun = 'full sun'   WHERE crop = 'garlic';
