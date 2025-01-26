{{ config(
    materialized='table'
) }}

SELECT DISTINCT
    region,
    manager,
    {{ add_timestamps() }}
FROM {{ ref('stg_managers') }}

