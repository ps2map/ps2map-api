-- Retrieve every continent whose map state is tracked in real-time.
SELECT
    "id",
    "name",
    "code",
    "description",
    "map_size"
FROM
    "api"."continent"
WHERE
    "name" IN (
        'Indar',
        'Esamir',
        'Amerish',
        'Hossin',
        'Oshur'
    )
;