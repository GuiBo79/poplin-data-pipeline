{% macro round_cast(expression, precision) %}
    ROUND(CAST({{ expression }} AS NUMERIC), {{ precision }})
{% endmacro %}