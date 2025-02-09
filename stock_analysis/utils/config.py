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
"DB_RAW_COLLECTION": os.getenv("DB_Raw_Collection"),
"DB_PROCESSED_COLLECTION": os.getenv("DB_Processed_Collection"),
"environment": os.getenv("NODE_ENV", "development"),
}

