
from utils.file_helpers import get_csv_path

def generate_csv_files(symbol, df):
    print(f"Generating csv files for {symbol}")
     # Create the subfolder for the symbol if it doesn't exist
    csv_path = get_csv_path(symbol)
    df.to_csv(csv_path, index=True)

    print(f"CSV report for {symbol} saved as {csv_path}")
    return str(csv_path)