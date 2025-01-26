{% macro filter_recent(date_column, years) %}
    {{ date_column }} >= CURRENT_DATE - INTERVAL '{{ years }} years'
{% endmacro %}
