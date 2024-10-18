-- SQL script to create a stored procedure named ComputeAverageWeightedScoreForUsers
-- This procedure computes and updates the average weighted score for all students

-- Drop the procedure if it already exists to avoid conflicts
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Change the delimiter to allow for the definition of the stored procedure
DELIMITER |

-- Create the stored procedure with no input parameters
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update the average_score column in the users table for each user
    UPDATE users
    SET average_score = (
        SELECT SUM(score * weight) / SUM(weight)  -- Calculate the weighted average score
        FROM corrections
        WHERE corrections.user_id = users.id  -- Filter scores based on the current user's ID
    );
END|

-- Reset the delimiter back to the default to end the procedure definition
DELIMITER ;
