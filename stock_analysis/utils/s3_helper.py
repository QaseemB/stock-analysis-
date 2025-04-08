import boto3
from botocore.exceptions import NoCredentialsError
from config.settings import config
import os


s3 = boto3.client('s3')
S3_BUCKET_NAME = config["S3_BUCKET"]

def get_s3_key(symbol,subfoler,filename):
    return f'STOCKMARKET_FBS / {symbol}/{subfoler}/{filename}'

def upload_file_to_s3(local_path, symbol, subfolder, filename):
    key = get_s3_key(symbol, subfolder, filename)
    try:
        s3.upload_file(str(local_path), S3_BUCKET_NAME, key)
        return f"s3://{S3_BUCKET_NAME}/{key}"
    except NoCredentialsError:
        print("AWS credentials not found.")
        return None

def save_pdf_to_s3(local_pdf_path,symbol):
    return upload_file_to_s3(local_pdf_path,symbol, 'pdf' ,f"{symbol}_report.pdf")

def save_csv_to_s3(local_csv_path, symbol):
    return upload_file_to_s3(local_csv_path,symbol, 'csv' ,f"{symbol}_report.csv")

def get_summary_json_path(symbol):
    return folder / f"{symbol}_summary.json"

def save_png_to_s3(local_png_path,symbol):
    return  upload_file_to_s3(local_png_path,symbol, 'png' ,f"{symbol}_report.png")

def save_plotly_to_s3(local_plotly_path,symbol,name):
    return upload_file_to_s3(local_plotly_path, symbol,'plotly',f"{symbol}_{name}.html")

def delete_local_file(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

def cleanup_s3_symbol_folder(symbol):
    prefix = f"stockmarket_fbs/{symbol}/"
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            s3.delete_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])