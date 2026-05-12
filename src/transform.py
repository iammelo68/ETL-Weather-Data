import pandas as pd
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
path_name = Path(__file__).parent.parent/'data'/'weather_data.json'

columns_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
    }
datetime_columns = ['datetime', 'sunrise', 'sunset']

def create_datagrame(path_name:str) -> pd.DataFrame:
    path = path_name
    if not path.exists():
        logging.error(f"File {path_name} does not exist.")
        return pd.DataFrame()
    
    with open(path) as f:
        data = json.load(f)
        df = pd.json_normalize(data)
    logging.info(f"Dataframe created with {len(df)} records.")
    return df

def normalize_columns(df:pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info("Columns normalized and merged into the main dataframe.")
    return df

def drop_columns(columns_to_drop:list[str], df:pd.DataFrame) -> pd.DataFrame:
    logging.info(f"Dropping columns: {columns_to_drop}")
    df = df.drop(columns=columns_to_drop)
    logging.info(f"Columns dropped. Remaining columns: {df.columns.tolist()}")
    return df

def rename_columns(df:pd.DataFrame, columns_to_rename:dict[str, str]) -> pd.DataFrame:
    df = df.rename(columns=columns_to_rename)
    logging.info(f"Columns renamed according to mapping: {columns_to_rename}")
    return df

def normalize_datetime_columns(df:pd.DataFrame, datetime_columns:list[str]) -> pd.DataFrame:
    for name in datetime_columns:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
        logging.info(f"Column '{name}' normalized to datetime format.")
    return df

def transform_weather_data():
    logging.info("Starting data transformation process.")
    df = create_datagrame(path_name)
    df = normalize_columns(df)
    df = drop_columns(columns_to_drop, df)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, datetime_columns)
    logging.info("Data transformation process completed.")
    return df