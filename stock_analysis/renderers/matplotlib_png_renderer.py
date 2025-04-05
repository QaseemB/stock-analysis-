import matplotlib.pyplot as plt
import os
import pandas as pd
from utils.file_helpers import create_png_folder


def bollinger_band(df,symbol):
     # Plot Close Price with Bollinger Bands
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df['close'], label='Close Price', color='blue')
    ax.plot(df.index, df['upper_band'], label='Upper Band', color='green', linestyle='--')
    ax.plot(df.index, df['lower_band'], label='Lower Band', color='red', linestyle='--')
    ax.fill_between(df.index, df['upper_band'], df['lower_band'], color='lightgray', alpha=0.5)
    ax.set_title(f"{symbol} Bollinger Bands Analysis")
    ax.xlabel("Date")
    ax.ylabel("Price")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

def macd(df,symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df['macd'], label="MACD", color="blue")
    ax.plot(df.index, df['signal_line'], label="Signal Line", color="red", linestyle="--")
    ax.set_title(f"{symbol} MACD Analysis")
    ax.xlabel("Date")
    ax.ylabel("MACD Value")
    ax.legend()
    return fig

def trade_volume(df,symbol):
    if 'volume' in df.columns:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.bar(df.index, df['volume'], color='gray', alpha=0.5)
        ax.set_title(f"{symbol} Trading Volume")
        ax.xlabel("Date")
        ax.ylabel("Volume")
        return fig
    return None

def moving_avg(df,symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df["close"], label="Close Price", color="blue")
    ax.plot(df.index, df["moving_avg_3"], label="3-Month Moving Average", linestyle="--", color="red")
    ax.plot(df.index, df["moving_avg_6"], label="6-Month Moving Average", linestyle="--", color="green")
    ax.plot(df.index, df["moving_avg_12"], label="12-Month Moving Average", linestyle="--", color="orange")
    ax.set_title(f"{symbol} Moving Averages")
    ax.xlabel("Date")
    ax.ylabel("Price")
    ax.legend()
    ax.grid(True)
    return fig

def generate_plots(symbol, df):
    print(f"Generating plots for {symbol}")
    
    # Ensure the index is datetime before plotting (if not already)
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    png_folder = create_png_folder(symbol)
    # Create a dictionary to store plot paths for different plots
    plot_paths = {} 

    plot_map = {
        "bollinger": bollinger_band,
        "macd": macd,
        "volume": trade_volume,
        "moving_avg": moving_avg
    }

    for name, plot_func in plot_map.items():
        try:
            fig = plot_func(df,symbol)

            # If fig is None (like in volume without 'volume' column), skip it
            if fig is None:
                print(f"skipping {name} plot (no data)")
                continue 
            
            plot_path = png_folder / f"{symbol}_{name}_plot.png"
            fig.savefig(plot_path)
            plot_paths[name] = str(plot_path)
            print(f"{name.capitalize()} plot saved ➡️ {plot_path}")
            plt.close(fig)
        except Exception as e:
            print(f"Error generating {name} plot: {e}")

            

    # Return all plot paths
    return plot_paths
