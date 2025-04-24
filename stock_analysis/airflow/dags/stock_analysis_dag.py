from airflow.decorators import dag, task
from datetime import datetime
import pendulum
from stock_analysis.renderers.interactive_plot_renderer import gen_interactive_plt
from stock_analysis.renderers.matplotlib_png_renderer import generate_plots
from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
# from stock_analysis.services.data_transformation import data_transformation
from stock_analysis.services.plot_generator import file_generation_parallel
from stock_analysis.services.store_transformed_data import store_transformed_data
from stock_analysis.services.csv_file_export import generate_csv_files

def chunk_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]

stock_list = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
  'IBM','TSLA','NVDA','AVGO','TSM','JPM','MA',
  'COST','PG','NFLX','JNJ','BAC','CRM','TM','KO','ORCL', 'D', 
  'HD','ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE',
  'AMD', 'T', 'VZ', 'DIS', 'NKE', 'PFE', 'PEP', 'CSCO', 'CMCSA', 'XOM', 
  'WMT', 'BMY', 'INTC', 'UNH', 'CVX', 'LLY', 'MCD', 'HON', 'NEE', 'TXN', 
  'PM', 'LOW', 'UPS', 'SCHW', 'MS', 'AMGN', 'CAT', 'GS', 'RTX', 'SPGI', 
  'BLK', 'BKNG', 'ISRG', 'MDT', 'SYK', 'LMT', 'DE', 'ADP', 'NOW', 'TMO', 
  'UNP', 'AMT', 'CB', 'CCI', 'ZTS', 'GILD', 'FIS', 'EL', 'MO', 'DUK', 
  'SO', 'MMM', 'BDX', 'APD', 'C', 'USB', 'PNC', 'CL', 'DHR', 'ITW', 'WM', 
  'SHW', 'ECL', 'FISV', 'AON', 'HUM', 'PSA', 'NSC', 'ETN', 'ROP', 'MAR', 
  'KMB', 'AEP', 'SBUX', 'LRCX', 'ATVI', 'ORLY', 'MCO', 'KLAC', 'CTAS', 
  'EQIX', 'ILMN', 'REGN', 'IDXX', 'MTD', 'CDNS', 'SNPS', 'FTNT', 'PAYC', 
  'ANSS', 'VRSK', 'MSCI', 'FLT', 'CPRT', 'TDG', 'WST', 'RMD', 'ALGN', 
  'STE', 'TECH', 'BIO', 'TER', 'KEYS', 'HUBS', 'SEDG', 'ENPH', 'TEAM', 
  'OKTA', 'ZS', 'CRWD', 'DDOG', 'DOCU', 'FSLY', 'NET', 'PLUG', 'BLD', 
  'PTON', 'ROKU', 'SQ', 'TWLO', 'U', 'ZM', 'ZSAN', 'VOO','QQQ','DIA', 'VTI'
];

batch1 = stock_list[0:25]
batch2 = stock_list[25:50]
batch3 = stock_list[50:75]
batch4 = stock_list[75:100]
batch5 = stock_list[100:125]
batch6 = stock_list[125:]


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 5, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    concurrency=1,
    tags=["analysis_pipeline"],
)
def stock_analysis_dag():


    @task()
    def generate_batch(symbols: list):
        file_generation_parallel(symbols)
        print(f"✅ Files generated for: {symbols}...")

    @task()
    def insert_batch(symbols: list):
        store_transformed_data(symbols)
        print(f"📥 Inserted to SQL: {symbols}...")

 
    # Create all batch task chains dynamically
    batches = chunk_list(stock_list, 10)
    for i, batch in enumerate(batches):
        generated = generate_batch.override(task_id=f"generate_batch_{i+1}")(batch)
        inserted = insert_batch.override(task_id=f"insert_batch_{i+1}")(batch)
        generated >> inserted  # link them


stock_analysis_dag = stock_analysis_dag()


