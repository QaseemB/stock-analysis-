from airflow.decorators import dag, task
from datetime import timedelta
import pendulum
import logging
from stock_analysis.services.summary_path import gen_summary_path
from stock_analysis.utils.stock_list import stock_list
from stock_analysis.services.plot_generator import file_generation_parallel
from stock_analysis.services.store_transformed_data import store_transformed_data
from stock_analysis.services.store_plotly_in_psql import plotly_insert_into_psql
from stock_analysis.services.backup_plotly_to_s3 import backup_plotly_to_s3

def chunk_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]



batch1 = stock_list[0:25]
batch2 = stock_list[25:50]
batch3 = stock_list[50:75]
batch4 = stock_list[75:100]
batch5 = stock_list[100:125]
batch6 = stock_list[125:]


@dag(
    schedule="0 0 1 * *",
    start_date=pendulum.datetime(2025, 1, 5, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    concurrency=1,
    default_args= {
        "retries":2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["analysis_pipeline"],
    description="DAG to batch-process stock data: generate plots, store in SQL, and summarize."
)

def stock_analysis_dag():


    @task()

    def generate_batch(symbols: list):
        file_generation_parallel(symbols)
        logging.info(f"✅ Files generated for: {symbols}...")
    
    @task()
    def summary_batch(symbols: list):
        gen_summary_path(symbols)
        logging.info(f'fsummary files are being generated for: {symbols}...')


    @task()
    def insert_batch(symbols: list):
        store_transformed_data(symbols)
        logging.info(f"📥 Inserted to SQL: {symbols}...")
    
    @task()
    def plotly_to_sql(symbols: list):
        plotly_insert_into_psql(symbols)
        logging.info(f"inserting Plotly plots for symbol: {symbols}, into sql")

    @task()
    def plotly_json_s3_backup():
        backup_plotly_to_s3()
        logging.info(f'backing up entire plotly json database to aws s3')
        

 
    # Create all batch task chains dynamically
    batches = chunk_list(stock_list, 10)
    previous_task = None
    for i, batch in enumerate(batches):
        generated = generate_batch.override(task_id=f"generate_batch_{i+1}")(batch)
        inserted = insert_batch.override(task_id=f"insert_batch_{i+1}")(batch)
        summary = summary_batch.override(task_id=f"summary_batch_{i+1}")(batch)
        plotly_sql = plotly_to_sql.override(task_id=f"plotly_to_sql_{i+1}")(batch)



        batch_chain = generated >> inserted >> summary  >> plotly_sql# link them

        # Keep track of the last task to chain backup afterward
        if previous_task:
            previous_task >> batch_chain

        previous_task = batch_chain
    # Only trigger backup once all batches are done
    backup = plotly_json_s3_backup.override(task_id="plotly_json_s3_backup")()
    previous_task >> backup

stock_analysis_dag = stock_analysis_dag()


