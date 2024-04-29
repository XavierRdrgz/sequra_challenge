with launches as (

    SELECT * FROM {{ ref('stg_spacex__launches' )}}

)


SELECT
  *
FROM launches
