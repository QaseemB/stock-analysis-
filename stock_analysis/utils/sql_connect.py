import psycopg2
import os
from utils.config import config

def connect_to_sql():
    
        # dbname= config["SQL_NAME"],
        # user= config["SQL_USER"],
        # password= config["SQL_PASSWORD"],
        # host= config["SQL_HOST"],
        # port= config["SQL_PORT"]
        url = config["DATABASE_URL"]
        print("🔎 DATABASE_URL from env:", os.getenv("DATABASE_URL"))

        
        if not url:
            raise ValueError("❌ DATABASE_URL is missing from config")
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://")
        return psycopg2.connect(url)

