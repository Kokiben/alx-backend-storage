-- Script to create a function named SafeDiv
-- that divides two integers and returns 0 if the second integer is 0.

DROP FUNCTION IF EXISTS SafeDiv;

DELIMITER $$

CREATE FUNCTION SafeDiv(
    a INT,
    b INT
) RETURNS FLOAT
BEGIN
    RETURN IF(b = 0, 0, a / b);
END$$

DELIMITER ;
