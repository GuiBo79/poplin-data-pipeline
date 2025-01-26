{{ config(materialized='table') }}

SELECT
    o.order_id,
    o.order_date,
    o.sales,
    o.profit,
    sales - profit AS cost,
    {{ calculate_discount('sales', 'profit') }} AS discount_pct,  -- Using the macro
    o.is_returned,
    o.refunded_sales,
    r.manager,
    {{ add_timestamps() }}  -- Add timestamps
FROM {{ ref('int_orders_with_returns') }} o
LEFT JOIN {{ ref('dim_regions') }} r
ON o.region = r.region
