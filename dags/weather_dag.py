from datetime import datetime, timedelta
from airflow.sdk import dag, task
from pathlib import Path
import sys, os

sys.path.insert(0, '/opt/airflow/src')

from extract import extract_weather_data
from transform import transform_weather_data
from load import load_weather_data

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)


API_KEY = os.getenv('API_KEY')
url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'

@dag(
    dag_id='weather_etl_dag',
    description='ETL pipeline for weather data',
    default_args={
            'owner': 'airflow',
            'depends_on_past': False,
            'retries': 2,
            'retry_delay': timedelta(minutes=5)
        },
    schedule='0 */1 * * *',
    start_date=datetime(2026, 5, 11),
    catchup=False,
    tags=['weather', 'etl']
)

def pipeline():
    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = transform_weather_data()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_weather_data(df, 'weather_data')


    extract() >> transform() >> load()

pipeline()
