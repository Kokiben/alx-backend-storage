-- Change the delimiter to allow for stored procedure definition
DELIMITER //

-- Create a stored procedure that computes the average weighted score for a user
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables to hold the total score, total weight, and the average weighted score
    DECLARE total_score DECIMAL(10, 2);
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE average_weighted_score DECIMAL(10, 2);

    -- Initialize the totals to zero
    SET total_score = 0;
    SET total_weight = 0;

    -- Calculate the total weighted score for the specified user
    SELECT SUM(score * weight) INTO total_score
    FROM scores  -- Table containing the scores and weights
    WHERE user_id = user_id;  -- Filter by the input user_id

    -- Calculate the total weight for the specified user
    SELECT SUM(weight) INTO total_weight
    FROM scores  -- Table containing the scores and weights
    WHERE user_id = user_id;  -- Filter by the input user_id

    -- Calculate the average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = total_score / total_weight;  -- Avoid division by zero
    ELSE
        SET average_weighted_score = 0; -- Handle case where there are no weights
    END IF;

    -- Store the result in a user_scores table or update if it already exists
    INSERT INTO user_scores (user_id, average_weighted_score)
    VALUES (user_id, average_weighted_score)  -- Insert new average score
    ON DUPLICATE KEY UPDATE average_weighted_score = average_weighted_score;  -- Update if user_id already exists

END //

-- Reset the delimiter back to the default
DELIMITER ;
