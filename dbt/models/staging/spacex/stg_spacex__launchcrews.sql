with source as (
    SELECT * FROM {{ source('raw_spacex','launchcrews') }}
),

renamed as (
    SELECT
        launch_id,
        crew as crew_id,
        "role"
    FROM source
)

SELECT * FROM renamed
