SELECT *
FROM {{ ref('stg_orders') }}
WHERE sales < 0
