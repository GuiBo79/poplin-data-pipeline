{{ config(materialized='view') }}

SELECT
    id,
    order_id,
    order_date,
    ship_date,
    customer_id,
    customer_name,
    region,
    category,
    sub_category,
    sales,
    profit,
    {{ calculate_discount('sales', 'profit') }} AS discount_pct,
    sales - profit AS cost,
    {{ add_timestamps() }}
FROM {{ source('cdc', 'orders') }}
