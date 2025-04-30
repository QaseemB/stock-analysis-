import psycopg2
import json
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError
# from pathlib import Path
from stock_analysis.utils.file_helpers import get_base_symbol_folder
from stock_analysis.utils.s3_helper import get_s3_key
from stock_analysis.utils.sql_connect import connect_to_sql
from stock_analysis.config.settings import config


s3 = boto3.client('s3')
S3_BUCKET_NAME = config["S3_BUCKET"]

def plotly_json_path(symbol, name):
    folder = get_base_symbol_folder(symbol) / 'plotly'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{symbol}_{name}.json"


def backup_plotly_to_s3():
    """
    backing up the enitre psql plotly database
    """
    conn = connect_to_sql()
    cursor = conn.cursor()

    cursor.execute('SELECT symbol,interactive_plot, created_at FROM stock_visualizations')
    records = cursor.fetchall()

    for symbol, plot_json_raw, created_at in records:
        try:
            date_str = created_at.strftime("%Y-%m-%d")
            filename = f"{symbol}_plotly_psql_.json"
            local_path = plotly_json_path(symbol, 'Plotly_psql')

            # Convert raw string into valid JSON
            plot_json = json.loads(plot_json_raw)

            with open(local_path, 'w') as f:
                json.dump(plot_json, f)

            s3_key = get_s3_key(symbol,'plotly',filename)
            s3.upload_file(str(local_path), S3_BUCKET_NAME,s3_key)
            print(f"✅ Uploaded: s3://{S3_BUCKET_NAME}/{s3_key}")
        except NoCredentialsError:
            print("AWS credentials not found.")
        except Exception as e:
            print(f"Error uploading {symbol}: {e}")
        
    cursor.close()
    conn.close()

# backup_plotly_to_s3()
