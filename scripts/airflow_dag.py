from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.exceptions import AirflowTaskTimeout
import logging
import subprocess
# /Users/airflow/dags/airflow_dag.py # this file must be on given path

dag = DAG(
    "my_dag",
    schedule="*/5 * * * *",
    start_date=datetime(2025, 2, 18),
    catchup=False,  
)

def run_producer():
    try:
        # Run the Producer script
        result = subprocess.run(
            ["python3", '/Users/kafka_airflow_spark_venv/scripts/producer.py'],
            check=True, capture_output=True, text=True
        )
        logging.info("Producer Output: %s", result.stdout)  # Log the output
    except subprocess.CalledProcessError as e:
        logging.error("Error occurred while running Producer: %s", e.stderr)  # Log the error output
        raise  # Re-raise the error to notify Airflow of the failure

def run_spark():
    try:
        result = subprocess.run(
            ["python3", '/Users/kafka_airflow_spark_venv/scripts/spark_consumer.py'],
            check=True, capture_output=True, text=True
        )
        logging.info("Spark Consumer Output: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("Error occurred while running Spark Consumer: %s", e.stderr)
        raise


start_kafka = BashOperator(
    task_id="start_kafka",
    bash_command="python3 /Users/kafka_airflow_spark_venv/scripts/start_kafka.py",
    dag=dag,
)

start_producer = PythonOperator(
    task_id="start_producer",
    python_callable=run_producer,
    execution_timeout=timedelta(minutes=10),  # Increase timeout
    on_failure_callback=lambda context: print("Task failed:", context["exception"]),
)

start_spark = PythonOperator(
    task_id="start_spark",
    python_callable=run_spark,
    dag=dag,
)

move_to_postgres = BashOperator(
    task_id="move_to_postgres",
    bash_command="python3 /Users/kafka_airflow_spark_venv/scripts/move_to_postgres.py",
    dag=dag,
)

# Define Task Dependencies
start_kafka >> start_producer >> start_spark >> move_to_postgres



