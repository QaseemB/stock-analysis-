import pandas as pd

def analyze_stock_data(monthly_data):
    df = pd.DataFrame(monthly_data)
    if df.empty:
        print("No data available for analysis.")
        return None

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    # Add analysis logic
    df["moving_avg_3"] = df["close"].rolling(window=3).mean()
    df["upper_band"] = df["close"].rolling(window=3).mean() + (df["close"].rolling(window=3).std() * 2)
    df["lower_band"] = df["close"].rolling(window=3).mean() - (df["close"].rolling(window=3).std() * 2)
    return df
