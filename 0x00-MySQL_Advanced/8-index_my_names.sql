-- This script creates an index on the first letter of the name column in the names table.
-- The index will be named idx_name_first.

-- Create the index on the first character of the name colum.
CREATE INDEX idx_name_first ON names(name(1));
