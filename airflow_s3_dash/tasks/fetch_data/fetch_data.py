import requests
import json
import pandas as pd
from datetime import datetime, timezone
import pytz


def convert_updated_to_date_time(x):
    # new_date_time = datetime.fromtimestamp(x/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    # return new_date_time
    # Convert timestamp(milliseconds) to datetime
    utc_timestamp = x / 1000  # Convert milliseconds to seconds
    utc_datetime = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
    
    # Convert time from UTC to Vietnam timezone (UTC+7)
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_datetime = utc_datetime.astimezone(vn_tz)
    
    # Format it into time string
    return vn_datetime.strftime("%Y-%m-%d %H:%M:%S")
def fetch_data():
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
        # df.to_csv(f'{out_put_path}', columns=['rank', 'exchangeId', 'name', 'percentTotalVolume','updated','exchangeUrl'], index=False)
        return df
    
    except requests.exceptions.RequestException as e:
        print(e)

def save_data(df, out_put_path):
    df.to_csv(f'{out_put_path}', columns=['rank', 'exchangeId', 'name', 'percentTotalVolume','updated','exchangeUrl'], index=False)
if __name__ == '__main__':
    out_put_path = r'/opt/airflow/data/coin_data.csv'
    df = fetch_data()
    save_data(df, out_put_path)