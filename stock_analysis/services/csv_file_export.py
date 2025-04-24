
from stock_analysis.utils.file_helpers import get_csv_path
from stock_analysis.utils.s3_helper import save_csv_to_s3, delete_local_file

def generate_csv_files(symbol, df):
    print(f"Generating csv files for {symbol}")

    # Drop the '_id' column if it exists (likely from MongoDB)
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # Reorder columns to move 'symbol' to the front if it exists
    if 'symbol' in df.columns:
        cols = df.columns.tolist()
        cols.insert(0, cols.pop(cols.index('symbol')))
        df = df[cols]
        
     # Create the subfolder for the symbol if it doesn't exist
    csv_path = get_csv_path(symbol)

    cols_to_round = [
    "open", "high", "low", "close", "volume",
    "moving_avg_3", "moving_avg_6", "moving_avg_12",
    "rolling_mean", "rolling_std", "upper_band", "lower_band",
    "monthly_return", "ema12", "ema26", "macd", "signal_line", "rsi"
]
    df[cols_to_round] = df[cols_to_round].round(2)
    df.to_csv(csv_path, index=True)

    print(f"CSV report for {symbol} saved as {csv_path}")

    s3_uri = save_csv_to_s3(csv_path,symbol)
    if s3_uri:
        delete_local_file(csv_path)
        print(f"local path to csv files for {symbol} have been delted and the file has be uploaded to s3")
    return str(s3_uri or csv_path)