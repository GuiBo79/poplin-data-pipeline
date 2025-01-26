{{ config(materialized='table') }}

SELECT
    o.region,
    COUNT(o.order_id) AS total_orders,
    SUM(o.sales) AS total_sales,
    SUM(o.profit) AS total_profit,
    AVG({{ calculate_discount('sales', 'profit') }}) AS avg_discount_pct,
    SUM(o.refunded_sales) AS total_refunds,
    {{ round_cast('SUM(o.refunded_sales) * 100.0 / NULLIF(SUM(o.sales), 0)', 2) }} AS refund_rate,
    {{ add_timestamps() }} 
FROM {{ ref('int_orders_with_returns') }} o
GROUP BY o.region
