{{ config(materialized='table') }}

WITH enriched_orders AS (
    SELECT
        o.order_id,
        o.order_date,
        o.sales,
        o.profit,
        o.region,
        sales - profit AS cost,
        {{ calculate_discount('sales', 'profit') }} AS discount_pct,  -- Using the macro
        COALESCE(r.is_returned, FALSE) AS is_returned,  -- Include return info
        {{ add_timestamps() }}  -- Add timestamps
    FROM {{ ref('stg_orders') }} o
    LEFT JOIN {{ ref('stg_returns') }} r
    ON o.order_id = r.order_id
)

SELECT
    *,
    CASE
        WHEN is_returned THEN sales  -- Total refunded sales
        ELSE 0
    END AS refunded_sales
FROM enriched_orders
