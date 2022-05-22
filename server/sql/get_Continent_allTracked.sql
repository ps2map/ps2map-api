-- Retrieve every continent whose map state is tracked in real-time.
SELECT
    "id",
    "name",
    "code",
    "description",
    "map_size"
FROM
    "API_static"."Continent"
WHERE
    "tracking_enabled" = true
;