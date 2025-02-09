import pandas as pd
import os 



def analyze_stock_data(monthly_data,symbol):
    
    symbol_folder = os.path.join('csv_report', symbol)
    os.makedirs(symbol_folder, exist_ok=True)

    df = pd.DataFrame(monthly_data)
    if df.empty:
        print("No data available for analysis.")
        return None

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

      # Moving Averages
    df["moving_avg_3"] = df["close"].rolling(window=3).mean()
    df["moving_avg_6"] = df["close"].rolling(window=6).mean()
    df["moving_avg_12"] = df["close"].rolling(window=12).mean()

    # Bollinger Bands
    rolling_window = 3
    df['rolling_mean'] = df['close'].rolling(window=rolling_window).mean()
    df['rolling_std'] = df['close'].rolling(window=rolling_window).std()
    df['upper_band'] = df['rolling_mean'] + (df['rolling_std'] * 2)
    df['lower_band'] = df['rolling_mean'] - (df['rolling_std'] * 2)

    # Monthly Returns
    df["monthly_return"] = df["close"].pct_change() * 100

    # MACD and Signal Line
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()

    # Drop NaN values from the DataFrame
    df.dropna(inplace=True)

    # Create the path for the CSV file for the specific symbol
    csv_path = os.path.join(symbol_folder, f"{symbol}_csv_report.csv")
    # Save the analyzed data to a CSV file within the symbol-specific folder
    df.to_csv(csv_path, index=True)
    print(f"CSV report for {symbol} saved to {csv_path}")
    

    return df
