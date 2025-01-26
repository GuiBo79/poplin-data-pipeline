FROM apache/airflow:2.6.3

# Switch to the airflow user
USER airflow

# Install dbt and PostgreSQL client libraries as the airflow user
RUN pip install --no-cache-dir dbt-core dbt-postgres

WORKDIR /opt/airflow/dbt
