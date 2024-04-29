with

source as (

    SELECT * FROM {{ source('raw_spacex','launchcores') }}

),

renamed as (

    SELECT
        launch_id,
        core as core_id,
        flight,
        gridfins,
        legs,
        reused,
        landing_attempt,
        landing_success,
        landing_type,
        landpad
    FROM source

)

SELECT * FROM renamed
