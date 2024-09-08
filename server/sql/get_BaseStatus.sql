SELECT
	"base_id",
	"server_id",
	"owning_faction_id",
	"owned_since"
FROM
	"api"."base_ownership"
WHERE
	"continent_id" = %s
AND
	"server_id" = %s
;