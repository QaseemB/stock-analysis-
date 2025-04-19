from airflow.decorators import dag, task
from datetime import datetime
import pendulum
from stock_analysis.renderers.interactive_plot_renderer import gen_interactive_plt
from stock_analysis.renderers.matplotlib_png_renderer import generate_plots
from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
# from stock_analysis.services.data_transformation import data_transformation
# from stock_analysis.services.plot_generator import file_generation
from stock_analysis.services.store_transformed_data import store_transformed_data
from stock_analysis.services.csv_file_export import generate_csv_files

# stock_list = [
#   'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
#   'IBM','TSLA','NVDA','AVGO','TSM','JPM','MA',
#   'COST','PG','NFLX','JNJ','BAC','CRM','TM','KO','ORCL', 'D', 
#   'HD','ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE',
#   'AMD', 'T', 'VZ', 'DIS', 'NKE', 'PFE', 'PEP', 'CSCO', 'CMCSA', 'XOM', 
#   'WMT', 'BMY', 'INTC', 'UNH', 'CVX', 'LLY', 'MCD', 'HON', 'NEE', 'TXN', 
#   'PM', 'LOW', 'UPS', 'SCHW', 'MS', 'AMGN', 'CAT', 'GS', 'RTX', 'SPGI', 
#   'BLK', 'BKNG', 'ISRG', 'MDT', 'SYK', 'LMT', 'DE', 'ADP', 'NOW', 'TMO', 
#   'UNP', 'AMT', 'CB', 'CCI', 'ZTS', 'GILD', 'FIS', 'EL', 'MO', 'DUK', 
#   'SO', 'MMM', 'BDX', 'APD', 'C', 'USB', 'PNC', 'CL', 'DHR', 'ITW', 'WM', 
#   'SHW', 'ECL', 'FISV', 'AON', 'HUM', 'PSA', 'NSC', 'ETN', 'ROP', 'MAR', 
#   'KMB', 'AEP', 'SBUX', 'LRCX', 'ATVI', 'ORLY', 'MCO', 'KLAC', 'CTAS', 
#   'EQIX', 'ILMN', 'REGN', 'IDXX', 'MTD', 'CDNS', 'SNPS', 'FTNT', 'PAYC', 
#   'ANSS', 'VRSK', 'MSCI', 'FLT', 'CPRT', 'TDG', 'WST', 'RMD', 'ALGN', 
#   'STE', 'TECH', 'BIO', 'TER', 'KEYS', 'HUBS', 'SEDG', 'ENPH', 'TEAM', 
#   'OKTA', 'ZS', 'CRWD', 'DDOG', 'DOCU', 'FSLY', 'NET', 'PLUG', 'BLD', 
#   'PTON', 'ROKU', 'SQ', 'TWLO', 'U', 'ZM', 'ZSAN', 'VOO','QQQ','DIA', 'VTI'
# ];

stock_list = ['ZM', 'ZSAN', 'VOO','QQQ','DIA', 'VTI']

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
    def get_stock_list():
        print(f'fetched stock list')
        return stock_list
    @task()
    def transform(symbol: str):
        raw_data = get_stock_data(symbol)
        if raw_data is None:
            print(f"❌ No data returned for {symbol}")
            return {"symbol": symbol, "df": None}
        df = analyze_stock_data(raw_data, symbol)
        if df is None:
            print(f"❌ Failed to analyze {symbol}")
        return {"symbol": symbol, "df": df}
    @task()
    def png_generator(symbol:str, df):
        if df is not None:
            generate_plots(symbol, df)
    @task 
    def plotly_generator(symbol:str, df):
        if df is not None:
            gen_interactive_plt(symbol, df)
        
    @task()
    def csv_generator(symbol:str, df):
        if df is not None:
            generate_csv_files(symbol, df)
        

    @task
    def insert_all_into_sql(symbol: list):
        store_transformed_data(stock_list)
        print(f'all symbols inserted into sql')
 

    symbols = get_stock_list()
    transformed = transform.expand(symbol=symbols)

    png_generator.expand(symbol=transformed["symbol"], df=transformed["df"])
    plotly_generator.expand(symbol=transformed["symbol"], df=transformed["df"])
    csv_generator.expand(symbol=transformed["symbol"], df=transformed["df"])

stock_analysis_dag = stock_analysis_dag()


