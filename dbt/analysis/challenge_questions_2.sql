-- Which cores have been reused in less than 50 days after the previous launch? Write
-- an SQL query to find the result.

SELECT
  core_id
FROM (
  SELECT
    core_id,
    launchcores.reused,
    launches.static_fire_date_utc,
    LAG(launches.static_fire_date_utc) OVER (
      PARTITION BY core_id
      ORDER BY launches.static_fire_date_utc ASC
    ) AS lag_fire_date_utc
  FROM {{ ref("launchcores") }} AS launchcores
  LEFT JOIN {{ ref("launches") }} AS launches USING (launch_id)
)
WHERE
  reused AND
  static_fire_date_utc - lag_fire_date_utc <= make_interval(days => 50)
