import psycopg2
import os
from stock_analysis.config.settings import config
from stock_analysis.utils.stock_list import stock_list

def connect_to_sql():
        env = config["environment"]
        if env == "production":         
            uri = config["RDS_DB_URL"]
            print("🔎 Connecting RDS DATABASE_URL")
        else:
             uri = config["LOCAL_DATABASE_URL"]
             print(f"🔎 Connecting to Local DATABASE URL")

        
        if not uri:
            raise ValueError("❌ DATABASE_URL is missing from config")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://")

        print(f"🔎 DATABASE URL:",uri)
        return psycopg2.connect(uri)

