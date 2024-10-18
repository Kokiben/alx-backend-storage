-- Create a view named 'need_meeting'
CREATE VIEW need_meeting AS
SELECT name  -- Select the name of the students
FROM students  -- From the 'students' table
WHERE score < 80  -- Filter for students with a score strictly under 80
AND (
    last_meeting IS NULL  -- Include students with no last meeting date
    OR last_meeting < NOW() - INTERVAL 1 MONTH  -- Include students whose last meeting was more than a month ago
);
