from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import requests
import json
import pandas as pd
from datetime import datetime, timezone
import pytz


with DAG(
    dag_id='Coin_project',
    start_date=datetime(2024, 8, 26)
    # schedule_interval='@daily'
) as dag:
    extract_data = BashOperator(
        task_id='fetch_data',
        bash_command='python /opt/airflow/tasks/fetch_data/fetch_data.py'
        # python_callable=fetch_data,
        # op_kwargs={
        #     'out_put_path': '/opt/airflow/data/coin_data.csv'
        # }
    )
    upload_to_minio = BashOperator(
        task_id='upload_to_minio',
        bash_command='python /opt/airflow/tasks/work_with_s3/upload_to_s3.py'
    )
extract_data >> upload_to_minio