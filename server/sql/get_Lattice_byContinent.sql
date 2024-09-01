-- Retrieve the base lattice links for a given continent.
SELECT
    "base_a_id",
    "base_b_id",
    "map_pos_a_x",
    "map_pos_a_y",
    "map_pos_b_x",
    "map_pos_b_y"
FROM
    "api"."lattice"
WHERE
    "continent_id" = %s
;