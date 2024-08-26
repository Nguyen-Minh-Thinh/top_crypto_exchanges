import dash
import os
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px 
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = '/tmp/.env'
load_dotenv(dotenv_path=env_path)


# Initialize dash application
app = dash.Dash(__name__)

# Endpoint to API
endpoint_url = 'http://host.docker.internal:9000'
access_key = os.getenv('S3_ACCESS_KEY')
secret_key = os.getenv('S3_SECRET_KEY')

# Initialize client
s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)
bucket_name = 'coin-project-bucket'
file_key = 'coin_data.csv'

def get_data_from_minio():
    try:
        # Get object from s3
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Read data from object and load to dataframe
        df = pd.read_csv(obj['Body'])

        df = df[df.percentTotalVolume > 0.5]    # Only show values > 0.5

        return df

    except Exception as e:
        print(f"Error reading file from S3: {str(e)}")
        return None

# App layout
app.layout = html.Div([
    html.Div(
        children='Data Table',
        style={'textAlign': 'center', 'marginTop': '20px', 'marginBottom': '20px', 'fontSize': '24px', 'color': '#007BFF'}
    ),
    dash_table.DataTable(id='table', page_size=10),
    html.Div(
        children='Phần trăm tổng khối lượng giao dịch của từng sàn trong thị trường (>0.5)',
        style={'textAlign': 'center', 'margin-top': '20px','fontSize': '24px', 'color': '#00008B'}
    ),
    dcc.Graph(id='graph'),
    dcc.Interval(
        id='interval-component',
        interval=10000,  # Cập nhật dữ liệu sau mỗi 5 phút
        n_intervals=0  # Bắt đầu với số lần gọi callback là 0
    )
])

# Callback to update data
@app.callback(
    [dash.dependencies.Output('table', 'data'),
     dash.dependencies.Output('graph', 'figure')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_data(n):
    df = get_data_from_minio()
    if df is not None:
        table_data = df.to_dict('records')
        fig = px.bar(df, x='exchangeId', y='percentTotalVolume', range_y=[0, 100])
        return table_data, fig
    else:
        return [], {}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
