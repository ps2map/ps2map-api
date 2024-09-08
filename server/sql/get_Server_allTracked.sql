-- Retrieve every continent.
SELECT
    "id",
    "name",
    "region",
    "platform"
FROM
    "api"."server"
WHERE
    "name" IN (
        'Connery',
        'Miller',
        'Cobalt',
        'Emerald',
        'SolTech',
        'Genudine',
        'Ceres'
    )
;