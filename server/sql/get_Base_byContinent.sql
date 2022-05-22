-- Retrieve every base on the given continent.
SELECT
    "id",
    "continent_id",
    "name",
    "map_pos_x",
    "map_pos_y",
    "type_name",
    "type_code",
    "resource_capture_amount",
    "resource_control_amount",
    "resource_name",
    "resource_code"
FROM
    "API_static"."BaseInfo"
WHERE
    "continent_id" = %s
;