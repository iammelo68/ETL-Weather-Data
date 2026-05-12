
# ETL - Weather Data

This Project is a ETL Pipeline based on [@vbuuiza](https://github.com/vbluuiza)'s YouTube [Tutorial](https://www.youtube.com/watch?v=I8qPqbXQBDU&t=3299s). It consumes OpenWeather API, normalize and transform data and load those information on a relational database (Postgresql)

## Stacks

### Core
- **Python 3.14+**
- **Apache Airflow 3.1.7**
- **PostgreSQL 14**
- **Docker & Docker Compose** 

### Python libraries
- **pandas**
- **requests**
- **SQLAlchemy**
- **psycopg2**
- **python-dotenv** 

### Outras Ferramentas
- **Redis** 
- **Jupyter Notebook** 
- **UV** 


## How to set

### 1 - Git Clone
Paste in your terminal the following command shell

``` 
git clone https://github.com/iammelo68/ETL-Weather-Data.git
cd ETL-Weather-Data
```

### 2 - Generate you API Key
Access [OpenWeatherMap](https://home.openweathermap.org/) and generate your API key for free.

### 3 - Set you enviroment
- Create your '.env' file inside '.config/':

```bash
# config/.env

# OpenWeatherMap API
API_KEY=sua_chave_api_aqui

# PostgreSQL
user=airflow
password=airflow
database=airflow
```
- Create the following directories:
```bash
mkdir -p ./dags ./logs ./plugins ./config ./data ./src ./notebooks
```

- Set up the necessary permissions (linux/Mac)
```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

-Start Docker Container
```bash
docker compose up -d
```

If it's all set, your environment is ready to be tested.

## How to use 
On your browser, search for **localhost:8080**

The default credencials are:
- **Username:** airflow
- **Password:** airflow

### How to trigger the pipelina

- Search for **Weather_dag**
- Trigger


## Author

[@iammelo68](https://www.github.com/iammelo68)

