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
        'Ceres',
        'Genudine',
        'Osprey',
        'SolTech',
        'Wainwright'
    )
;