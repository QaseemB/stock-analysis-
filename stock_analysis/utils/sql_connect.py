import psycopg2
from utils.config import config

def connect_to_sql():
    return psycopg2.connect(
        dbname= config["SQL_NAME"],
        user= config["SQL_USER"],
        password= config["SQL_PASSWORD"],
        host= config["SQL_HOST"],
        port= config["SQL_PORT"]
        )