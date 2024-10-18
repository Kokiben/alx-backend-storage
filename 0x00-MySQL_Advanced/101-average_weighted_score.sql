-- SQL script to create a stored procedure named ComputeAverageWeightedScoreForUsers
-- This procedure computes and updates the average weighted score for all students

-- Drop the procedure if it already exists to avoid conflicts
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Change the delimiter to allow for the definition of the stored procedure
DELIMITER |

-- Create the stored procedure with no input parameters
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  -- Update the average_score column in the users table (aliased as 'i')
  UPDATE users AS i, 
    -- Subquery to calculate the weighted average score for each user
    (SELECT i.id, SUM(score * weight) / SUM(weight) AS w_avg 
     FROM users AS i 
     JOIN corrections AS a ON i.id = a.user_id  -- Join corrections table to link user IDs with scores
     JOIN projects AS ol ON a.project_id = ol.id  -- Join projects table to include project data
     GROUP BY i.id) AS ji  -- Group results by user ID to get individual averages
  SET i.average_score = ji.w_avg  -- Update the average_score in the users table with the computed weighted average
  WHERE i.id = ji.id;  -- Ensure the update targets the correct user based on the ID
END|

-- Reset the delimiter back to the default to conclude the procedure definition
DELIMITER ;
