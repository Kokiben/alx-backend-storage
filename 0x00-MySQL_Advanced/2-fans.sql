-- SQL script to rank the origins of bands by total number of fans
-- Columns: origin and nb_fans
SELECT origin, SUM(nb_fans) AS nb_fans FROM metal_bands 
GROUP BY origin ORDER BY nb_fans DESC;
