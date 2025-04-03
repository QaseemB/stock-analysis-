import psycopg2
import os
from utils.config import config

def connect_to_sql():
    
        # dbname= config["SQL_NAME"],
        # user= config["SQL_USER"],
        # password= config["SQL_PASSWORD"],
        # host= config["SQL_HOST"],
        # port= config["SQL_PORT"]
        url = os.getenv("DATABASE_URL")
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://")
        return psycopg2.connect(url)