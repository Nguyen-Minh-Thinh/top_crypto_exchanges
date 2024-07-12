from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import requests
import json
import pandas as pd
from datetime import datetime, timezone
import pytz


def convert_updated_to_date_time(x):
    # new_date_time = datetime.fromtimestamp(x/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    # return new_date_time
    # Chuyển đổi timestamp từ milliseconds sang datetime
    utc_timestamp = x / 1000  # Chia cho 1000 để chuyển từ milliseconds sang seconds
    utc_datetime = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
    
    # Áp dụng múi giờ của Việt Nam (UTC+7)
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_datetime = utc_datetime.astimezone(vn_tz)
    
    # Format lại thành chuỗi thời gian
    return vn_datetime.strftime("%Y-%m-%d %H:%M:%S")
def fetch_data(**kwargs):
    out_put_path = kwargs['out_put_path']
    url = "https://api.coincap.io/v2/exchanges"
    try:
        # Extract
        response = requests.get(url)
        response.raise_for_status() 
        text = response.text
        data_dict = json.loads(text)    
        data = data_dict['data']
        
        # Transform
        df = pd.DataFrame(data)
        df['updated'] = df['updated'].apply(lambda x: convert_updated_to_date_time(x))

        df['percentTotalVolume'] = df['percentTotalVolume'].apply(lambda x: round(float(x), 3) if x is not None else x)
        
        # Load
        df.to_csv(f'{out_put_path}', columns=['rank', 'exchangeId', 'name', 'percentTotalVolume','updated','exchangeUrl'], index=False)
        
    except requests.exceptions.RequestException as e:
        print(e)
    

with DAG(
    dag_id='Coin_project',
    start_date=datetime(2024, 7, 9)
    # schedule_interval='@daily'
) as dag:
    extract_data = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
        op_kwargs={
            'out_put_path': '/opt/airflow/data/coin_data.csv'
        }
    )
    upload_to_minio = BashOperator(
        task_id='upload_to_minio',
        bash_command='python /opt/airflow/s3_bucket.py'
    )
extract_data >> upload_to_minio