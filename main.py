from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.load import load_weather_data

import os
from pathlib import Path
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent/'config'/'.env'
load_dotenv(dotenv_path=env_path)


API_KEY = os.getenv('API_KEY')

url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'
table_name = 'weather_data'

def pipeline():
    try:
        logging.info("Starting ETL pipeline.")
        extract_weather_data(url)
        df_transformed = transform_weather_data()
        load_weather_data(df_transformed, table_name)
        logging.info("ETL pipeline completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the ETL pipeline: {e}")
        import traceback
        traceback.print_exc()
    
pipeline()
