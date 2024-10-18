-- SQL script to create a stored procedure named ComputeAverageWeightedScoreForUser
-- This procedure computes and updates the average weighted score for a student in the users table

-- Drop the procedure if it already exists to avoid conflicts
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Change the delimiter to allow for the definition of the stored procedure
DELIMITER |

-- Create the stored procedure that takes a user ID as input
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT  -- Input parameter representing the user's ID
)
BEGIN
    -- Update the average_score column in the users table for the specified user
    UPDATE users
    SET avr_scr = (
        SELECT AVG(score)  -- Calculate the average of scores from the corrections table
        FROM corrections
        WHERE corrections.user_id = user_id  -- Filter scores based on the provided user ID
    )
    WHERE id = user_id;  -- Target the user in the users table with the matching user ID
END|

-- Reset the delimiter back to the default to end the procedure definition
DELIMITER ;
