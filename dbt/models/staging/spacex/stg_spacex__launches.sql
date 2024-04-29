with source as (
  SELECT * FROM {{ source('raw_spacex','launches') }}
)

SELECT
  fairings,
  links,
  TO_TIMESTAMP(static_fire_date_utc, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS static_fire_date_utc,
  static_fire_date_unix,
  tdb,
  net,
  "window",
  rocket,
  success,
  failures,
  details,
  ships,
  capsules,
  payloads,
  launchpad,
  auto_update,
  flight_number,
  name,
  TO_TIMESTAMP(date_utc, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS date_utc,
  date_unix,
  date_local,
  date_precision,
  upcoming,
  tbd,
  launch_library_id,
  id as launch_id
FROM source
