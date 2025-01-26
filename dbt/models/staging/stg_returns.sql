{{ config(materialized='view') }}

SELECT
    order_id,
    CASE WHEN returned = 'Yes' THEN TRUE ELSE FALSE END AS is_returned,
    {{ add_timestamps() }}
FROM {{ source('cdc', 'returns') }}

