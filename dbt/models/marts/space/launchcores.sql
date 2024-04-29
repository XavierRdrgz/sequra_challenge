with cores as (

    SELECT * FROM {{ ref('stg_spacex__launchcores' )}}

)


SELECT
  *
FROM cores
