-- Retrieve every continent.
SELECT
    "id",
    "name",
    "region",
    "platform"
FROM
    "API_static"."Server"
WHERE
    "tracking_enabled" = true
;