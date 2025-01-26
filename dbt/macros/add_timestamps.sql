{% macro add_timestamps() %}
    CURRENT_TIMESTAMP AS created_at,
    CURRENT_TIMESTAMP AS updated_at
{% endmacro %}