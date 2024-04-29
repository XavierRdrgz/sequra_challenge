-- List the months in which there has been more than one launch. Write an SQL query to
-- find the results.

SELECT
  EXTRACT(YEAR FROM static_fire_date_utc) AS year,
  EXTRACT(MONTH FROM static_fire_date_utc) AS month,
  COUNT(*) AS num_launches
FROM {{ ref("launches") }}
WHERE
  static_fire_date_utc IS NOT NULL
GROUP BY
  month, year
HAVING
  COUNT(*) > 1
ORDER BY
  year, month asc
