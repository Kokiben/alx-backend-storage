-- SQL script to list all Glam rock bands ranked by their longevity
-- Columns: band_name and lifespan (in years until 2022 or split)
SELECT band_name,
       (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
