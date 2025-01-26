{% macro calculate_discount(sales_column, profit_column) %}
    ({{ sales_column }} - {{ profit_column }}) / NULLIF({{ sales_column }}, 0) * 100
{% endmacro %}
