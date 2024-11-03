import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import plotly.express as px

# Load environment variables from .env
load_dotenv()

# Function to analyze and plot data for a specific stock symbol
def analyze_stock(symbol):
    ATLAS_URI = os.getenv('ATLAS_URI')
    client = MongoClient(ATLAS_URI)
    db = client['StockMarket']
    collection = db['historicalstocks']

    # Retrieve data
    stock_data = collection.find_one({"symbol": symbol})
    if not stock_data:
        print(f"No data found for {symbol}")
        return

    # Create DataFrame from retrieved data
    df = pd.DataFrame(stock_data["monthlyData"])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Sort the data by date
    df.sort_index(inplace=True)

    # Calculate moving averages
    df["moving_avg_3"] = df["close"].rolling(window=3).mean()
    df["moving_avg_6"] = df["close"].rolling(window=6).mean()
    df["moving_avg_12"] = df["close"].rolling(window=12).mean()

    # Calculate Bollinger Bands
    rolling_window = 3
    df['rolling_mean'] = df['close'].rolling(window=rolling_window).mean()
    df['rolling_std'] = df['close'].rolling(window=rolling_window).std()
    df['upper_band'] = df['rolling_mean'] + (df['rolling_std'] * 2)
    df['lower_band'] = df['rolling_mean'] - (df['rolling_std'] * 2)

    # Calculate monthly returns
    df["monthly_return"] = df["close"].pct_change() * 100

    # Calculate MACD and Signal Line
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()

    # Plot using matplotlib
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df["close"], label="Close Price", color="blue")
    plt.plot(df.index, df["moving_avg_3"], label="3-Month Moving Average", linestyle="--", color="red")
    plt.plot(df.index, df["upper_band"], label="Upper Bollinger Band", linestyle="--", color="green")
    plt.plot(df.index, df["lower_band"], label="Lower Bollinger Band", linestyle="--", color="orange")
    plt.fill_between(df.index, df['upper_band'], df['lower_band'], color='lightgrey', alpha=0.5)
    plt.title(f"{symbol} Stock Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

    # Plot volume data if available
    if 'volume' in df.columns:
        plt.figure(figsize=(14, 3))
        plt.bar(df.index, df['volume'], color='gray', alpha=0.5)
        plt.title(f"{symbol} Trading Volume")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.show()

    # Plot MACD
    plt.figure(figsize=(14, 5))
    plt.plot(df.index, df['macd'], label="MACD", color="blue")
    plt.plot(df.index, df['signal_line'], label="Signal Line", color="red", linestyle="--")
    plt.title(f"{symbol} MACD Analysis")
    plt.xlabel("Date")
    plt.ylabel("MACD Value")
    plt.legend()
    plt.show()

    # Interactive plot using Plotly
    fig = px.line(df, x=df.index, y=["close", "moving_avg_3", "moving_avg_6", "upper_band", "lower_band"],
                  title=f"{symbol} Interactive Stock Analysis")
    fig.update_layout(xaxis_title="Date", yaxis_title="Price")
    fig.show()

    # Print summary statistics
    print(f"Summary for {symbol}:")
    print(df.describe())

# List of stocks to analyze
stock_symbols = ['AAPL', 'GOOG', 'AMZN', 'META', 'MSFT', 'TSLA', 'IBM']
for symbol in stock_symbols:
    analyze_stock(symbol)
