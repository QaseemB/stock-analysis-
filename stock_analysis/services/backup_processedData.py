import csv
import boto3
import os
from stock_analysis.config.settings import config
from stock_analysis.utils.sql_connect import connect_to_sql
from stock_analysis.utils.s3_helper import get_s3_key


s3 = boto3.client('s3')
S3_BUCKET_NAME = config["S3_BUCKET"]

def backup_processed_data_to_s3():
    conn = connect_to_sql()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stock_analysis')
    records = cursor.fetchall()

    
