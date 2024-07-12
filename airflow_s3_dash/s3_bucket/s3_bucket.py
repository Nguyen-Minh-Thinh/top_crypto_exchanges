import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = '/opt/airflow/.env'
load_dotenv(dotenv_path=env_path)

# Access environment variables
access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_SECRET_KEY")
bucket_name = os.getenv("S3_BUCKET_NAME")
# print(type(access_key))
# print(type(secret_key))
# print(type(bucket_name))
file_path = '/opt/airflow/data/coin_data.csv'
object_name = 'coin_data.csv'
endpoint_url = 'http://host.docker.internal:9000'  # URL của MinIO, thay đổi nếu cần
try:
    # Khởi tạo client của S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url
    )
    # Upload file
    response = s3_client.upload_file(file_path, bucket_name, object_name)
    print(f'File uploaded successfully to bucket: {bucket_name}')
except NoCredentialsError:
    print('Credentials not available or incorrect.')




    
    