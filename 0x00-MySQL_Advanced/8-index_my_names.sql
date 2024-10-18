-- This script creates an index on the first letter of the name column in the names table.
-- The index will be named idx_name_first.

-- Drop the index if it already exists to avoid duplication errors.
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create the index on the first character of the name column.
CREATE INDEX idx_name_first ON names (name(1));
