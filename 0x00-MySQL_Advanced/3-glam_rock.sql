-- SQL script to list all Glam rock bands ranked by their longevity
-- Columns: band_name and lifespan (in years until 2022)
SELECT band_name, 
       (2022 - formed) AS lifespan 
FROM metal_bands 
WHERE style = 'Glam rock' 
ORDER BY lifespan DESC;
