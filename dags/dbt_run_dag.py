from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dbt_run_with_tests",
    default_args=default_args,
    description="Run dbt models with tests using Airflow",
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Run dbt models
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt",
    )

    # Task 2: Run dbt tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt",
    )

    # Task 3: Generate dbt documentation
    dbt_docs_generate = BashOperator(
        task_id="dbt_docs_generate",
        bash_command="dbt docs generate --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt",
    )

    dbt_run >> dbt_test >> dbt_docs_generate
