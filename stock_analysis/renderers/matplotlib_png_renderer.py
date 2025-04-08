import matplotlib.pyplot as plt
import os
import pandas as pd
from utils.file_helpers import get_png_folder
from utils.s3_helper import save_png_to_s3, delete_local_file, upload_file_to_s3


def bollinger_band(df,symbol):
     # Plot Close Price with Bollinger Bands
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df['close'], label='Close Price', color='blue')
    ax.plot(df.index, df['upper_band'], label='Upper Band', color='green', linestyle='--')
    ax.plot(df.index, df['lower_band'], label='Lower Band', color='red', linestyle='--')
    ax.fill_between(df.index, df['upper_band'], df['lower_band'], color='lightgray', alpha=0.5)
    ax.set_title(f"{symbol} Bollinger Bands Analysis")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

def macd(df,symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df['macd'], label="MACD", color="blue")
    ax.plot(df.index, df['signal_line'], label="Signal Line", color="red", linestyle="--")
    ax.set_title(f"{symbol} MACD Analysis")
    ax.set_xlabel("Date")
    ax.set_ylabel("MACD Value")
    ax.legend()
    return fig

def trade_volume(df,symbol):
    if 'volume' in df.columns:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.bar(df.index, df['volume'], color='gray', alpha=0.5)
        ax.set_title(f"{symbol} Trading Volume")
        ax.set_xlabel("Date")
        ax.set_ylabel("Volume")
        return fig
    return None

def moving_avg(df,symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df["close"], label="Close Price", color="blue")
    ax.plot(df.index, df["moving_avg_3"], label="3-Month Moving Average", linestyle="--", color="red")
    ax.plot(df.index, df["moving_avg_6"], label="6-Month Moving Average", linestyle="--", color="green")
    ax.plot(df.index, df["moving_avg_12"], label="12-Month Moving Average", linestyle="--", color="orange")
    ax.set_title(f"{symbol} Moving Averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    return fig

def rsi_plot(df, symbol):
    if "rsi" not in df.columns:
        print(f"Skipping RSI plot for {symbol} — RSI not found in DataFrame.")
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df["rsi"], label="RSI", color="purple")
    ax.axhline(70, color='red', linestyle='--', linewidth=1)
    ax.axhline(30, color='green', linestyle='--', linewidth=1)
    ax.set_title(f"{symbol} RSI (Relative Strength Index)")
    ax.set_xlabel("Date")
    ax.set_ylabel("RSI Value")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

def obv_plot(df, symbol):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['obv'], label="OBV", color="brown")
    ax.set_title(f"{symbol} On-Balance Volume")
    ax.set_xlabel("Date")
    ax.set_ylabel("OBV Value")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig



def generate_plots(symbol, df):
    print(f"Generating plots for {symbol}")
    # Ensure the index is datetime before plotting (if not already)
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    png_folder = get_png_folder(symbol)
    # Create a dictionary to store plot paths for different plots
    plot_paths = {} 

    plot_map = {
        "bollinger": bollinger_band,
        "macd": macd,
        "volume": trade_volume,
        "moving_avg": moving_avg,
        "Rsi": rsi_plot,
        "Obv": obv_plot

    }

    for name, plot_func in plot_map.items():
        try:
            fig = plot_func(df,symbol)

            # If fig is None (like in volume without 'volume' column), skip it
            if fig is None:
                print(f"skipping {name} plot (no data)")
                continue 
            
            plot_path = png_folder / f"{symbol}_{name}_plot.png"
            fig.savefig(plot_path, dpi=150)
            plot_paths[name] = str(plot_path)
            print(f"{name.capitalize()} plot saved ➡️ {plot_path}")
            plt.close(fig)
            filename = f"{symbol}_{name}_plot.png"
            s3_uri = upload_file_to_s3(plot_path,symbol,'png',filename)
            if s3_uri:
                delete_local_file(plot_path)
                print(f"local path to png files for {symbol} has been deleted and the files have been uploaded to s3 succefully")
        except Exception as e:
            print(f"Error generating {name} plot: {e}")

            

    # Return all plot paths
    return plot_paths
