{{ config(
    materialized='view'
) }}

SELECT
    manager,
    region,
    {{ add_timestamps() }}
FROM {{ source('cdc', 'managers') }}
WHERE region IS NOT NULL

