-- Retrieve the base lattice links for a given continent.
SELECT
    "base_id_a",
    "base_id_b"
FROM 
    "API_static"."LatticeLink"
WHERE
    "continent_id" = %s
;