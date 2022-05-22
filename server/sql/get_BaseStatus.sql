SELECT
	"base_id",
	"server_id",
	"owning_faction_id",
	"owned_since"
FROM
	"API_dynamic"."BaseOwnership"
LEFT JOIN
	"API_static"."Base"
	ON
		"base_id" = "id"
WHERE
	"continent_id" = %s
AND
	"server_id" = %s
;