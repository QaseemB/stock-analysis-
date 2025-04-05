import os
from dotenv import load_dotenv

load_dotenv()

config = {
"APIKEY": os.getenv("APIKEY"),
"APIKEY2": os.getenv("API_KEY2"),
"ATLASURI": os.getenv("ATLAS_URI"),
"PORT": os.getenv("PORT"),
"AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
"AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
"S3_REGION": os.getenv("S3_REGION"),
"S3_BUCKET": os.getenv("S3_BUCKET"),
"BASE_URL": "https://www.alphavantage.co/query",
"DB_NAME": os.getenv("DB_NAME"),
"DATABASE_URL": os.getenv("DATABASE_URL"),
"DB_RAW_COLLECTION": os.getenv("DB_Raw_Collection"),
"DB_PROCESSED_COLLECTION": os.getenv("DB_Processed_Collection"),
"environment": os.getenv("NODE_ENV", "development"),
"SQL_NAME": os.getenv("SQL_NAME"),
"SQL_USER": os.getenv("SQL_USER"),
"SQL_PASSWORD": os.getenv("SQL_PASSWORD"),
"SQL_HOST": os.getenv("SQL_HOST"),
"SQL_PORT": os.getenv("SQL_PORT"),
"SQL_DB": os.getenv("SQL_DB"),
"SQL_TABLE_NAME": os.getenv("SQL_TABLE_NAME"),   
"SQL_TABLE_ANALYSIS": os.getenv("SQL_TABLE_NAME_ANALYSIS"),
"PYTHON_FILE_BASE_SYS": os.getenv("PYTHON_FILE_BASE_SYS")
}

