-- This script creates a stored procedure named ComputeAverageScoreForUser
-- which calculates and updates the average score for a specified student.

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score) 
        FROM corrections
        WHERE corrections.user_id = user_id
    )
    WHERE id = user_id;
END$$

DELIMITER ;
