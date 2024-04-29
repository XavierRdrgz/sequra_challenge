-- Each time a rocket is launched, one or more cores (first stages) are involved.
-- Sometimes, cores are recovered after the launch and reused posteriorly in another
-- launch. What is the maximum number of times a core has been used? Write an SQL
-- query to find the result.

SELECT
  core_id,
  count(distinct launch_id) AS max_uses
FROM {{ ref('launchcores') }} launchcores
GROUP BY core_id
ORDER BY max_uses DESC
