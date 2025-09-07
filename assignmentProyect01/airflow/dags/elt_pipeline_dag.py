from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine

from src.extract import extract
from src.load import load
from src.transform import run_queries
import src.config as config

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

def extract_task():
    csv_folder = config.DATASET_ROOT_PATH
    csv_table_mapping = config.get_csv_to_table_mapping()
    public_holidays_url = config.PUBLIC_HOLIDAYS_URL
    return extract(csv_folder, csv_table_mapping, public_holidays_url)

def load_task(**context):
    data_frames = context['ti'].xcom_pull(task_ids='extract_task')
    engine = create_engine(f"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}")
    load(data_frames, engine)

def transform_task():
    engine = create_engine(f"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}")
    run_queries(engine)

with DAG(
    dag_id='elt_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='extract_task',
        python_callable=extract_task
    )

    t2 = PythonOperator(
        task_id='load_task',
        python_callable=load_task,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id='transform_task',
        python_callable=transform_task
    )

    t1 >> t2 >> t3
