from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

# Default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="incremental_load_with_schema",
    default_args=default_args,
    description="Incrementally load data from source DB to the warehouse with a custom schema",
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Create the `cdc` schema in the warehouse
    create_schema_task = PostgresOperator(
        task_id="create_cdc_schema",
        postgres_conn_id="warehouse_db",
        sql="CREATE SCHEMA IF NOT EXISTS cdc;",
    )

    # Create tables in the `cdc` schema
    create_tables_task = PostgresOperator(
        task_id="create_cdc_tables",
        postgres_conn_id="warehouse_db",
        sql="""
        CREATE TABLE IF NOT EXISTS cdc.orders (
            id SERIAL PRIMARY KEY,
            order_id TEXT,
            order_date DATE,
            ship_date DATE,
            ship_mode TEXT,
            customer_id TEXT,
            customer_name TEXT,
            segment TEXT,
            country TEXT,
            city TEXT,
            state TEXT,
            postal_code INTEGER,
            region TEXT,
            product_id TEXT,
            category TEXT,
            sub_category TEXT,
            product_name TEXT,
            sales FLOAT,
            quantity INTEGER,
            discount FLOAT,
            profit FLOAT
        );

        CREATE TABLE IF NOT EXISTS cdc.managers (
            manager TEXT,
            region TEXT
        );

        CREATE TABLE IF NOT EXISTS cdc.returns (
            returned TEXT,
            order_id TEXT
        );
        """,
    )

    def incremental_load(table_name, key_column, **kwargs):
        """
        Python function to perform an incremental load from source to warehouse.
        """
        source_hook = PostgresHook(postgres_conn_id="source_db")
        warehouse_hook = PostgresHook(postgres_conn_id="warehouse_db")

        # Determine the last loaded value from the warehouse
        last_loaded_query = f"SELECT COALESCE(MAX({key_column}), '2000-01-01') FROM cdc.{table_name};"
        last_loaded = warehouse_hook.get_first(last_loaded_query)[0]

        # Extract new data from the source
        extract_query = f"""
            SELECT * FROM {table_name}
            WHERE {key_column} > '{last_loaded}';
        """
        rows = source_hook.get_records(extract_query)

        # Load new data into the warehouse
        if rows:
            insert_query = f"""
                INSERT INTO cdc.{table_name} VALUES %s
            """
            warehouse_hook.insert_rows(table=f"cdc.{table_name}", rows=rows)

    # PythonOperator to incrementally load each table
    load_orders_task = PythonOperator(
        task_id="load_orders",
        python_callable=incremental_load,
        op_kwargs={"table_name": "orders", "key_column": "order_date"},
    )

    load_managers_task = PythonOperator(
        task_id="load_managers",
        python_callable=incremental_load,
        op_kwargs={"table_name": "managers", "key_column": "region"},
    )

    load_returns_task = PythonOperator(
        task_id="load_returns",
        python_callable=incremental_load,
        op_kwargs={"table_name": "returns", "key_column": "order_id"},
    )

    # Define task dependencies
    create_schema_task >> create_tables_task >> [load_orders_task, load_managers_task, load_returns_task]
