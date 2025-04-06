import pandas as pd

def moving_averages(df):
        # Moving Averages
    df["moving_avg_3"] = df["close"].rolling(window=3).mean()
    df["moving_avg_6"] = df["close"].rolling(window=6).mean()
    df["moving_avg_12"] = df["close"].rolling(window=12).mean()
    return df

def bollinger_bands(df):
    # Bollinger Bands
    rolling_window = 3
    df['rolling_mean'] = df['close'].rolling(window=rolling_window).mean()
    df['rolling_std'] = df['close'].rolling(window=rolling_window).std()
    df['upper_band'] = df['rolling_mean'] + (df['rolling_std'] * 2)
    df['lower_band'] = df['rolling_mean'] - (df['rolling_std'] * 2)
    return df 

def monthly_returns(df):
     # Monthly Returns
    df["monthly_return"] = df["close"].pct_change() * 100
    return df

def macd_signal_line(df):
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
    return df
    
    
    


def analyze_stock_data(cleaned_monthly_data,symbol):

    df = pd.DataFrame(cleaned_monthly_data)
    if df.empty:
        print("No data available for analysis.")
        return None

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    moving_averages(df)
     # Bollinger Bands
    bollinger_bands(df)
    # Monthly Returns
    monthly_returns(df)
    # MACD and Signal Line
    macd_signal_line(df)
    # Drop NaN values from the DataFrame
    df.dropna(inplace=True)
    return df