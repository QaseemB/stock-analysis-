import matplotlib.pyplot as plt
import os

def generate_plots(symbol, df):
    print(f"Generating plots for {symbol}")
    
    # Create a dictionary to store plot paths for different plots
    plot_paths = {}

    # Plot Close Price with Bollinger Bands
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close Price', color='blue')
    plt.plot(df.index, df['upper_band'], label='Upper Band', color='green', linestyle='--')
    plt.plot(df.index, df['lower_band'], label='Lower Band', color='red', linestyle='--')
    plt.fill_between(df.index, df['upper_band'], df['lower_band'], color='lightgray', alpha=0.5)
    plt.title(f"{symbol} Bollinger Bands Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    bollinger_plot_path = os.path.join('stockreport', f"{symbol}_bollinger_plot.png")
    try:
        plt.savefig(bollinger_plot_path)
        plot_paths['bollinger'] = bollinger_plot_path
        print(f"Bollinger plot saved as {bollinger_plot_path}")
    except Exception as e:
        print(f"Error saving Bollinger plot: {e}")
    plt.close()

    # Plot MACD
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['macd'], label="MACD", color="blue")
    plt.plot(df.index, df['signal_line'], label="Signal Line", color="red", linestyle="--")
    plt.title(f"{symbol} MACD Analysis")
    plt.xlabel("Date")
    plt.ylabel("MACD Value")
    plt.legend()
    macd_plot_path = os.path.join('stockreport', f"{symbol}_macd_plot.png")
    try:
        plt.savefig(macd_plot_path)
        plot_paths['macd'] = macd_plot_path
        print(f"MACD plot saved as {macd_plot_path}")
    except Exception as e:
        print(f"Error saving MACD plot: {e}")
    plt.close()

    # Plot Trading Volume
    if 'volume' in df.columns:
        plt.figure(figsize=(12, 3))
        plt.bar(df.index, df['volume'], color='gray', alpha=0.5)
        plt.title(f"{symbol} Trading Volume")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        volume_plot_path = os.path.join('stockreport', f"{symbol}_volume_plot.png")
        try:
            plt.savefig(volume_plot_path)
            plot_paths['volume'] = volume_plot_path
            print(f"Volume plot saved as {volume_plot_path}")
        except Exception as e:
            print(f"Error saving Volume plot: {e}")
        plt.close()

    # Plot Moving Averages (3, 6, 12 months)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["close"], label="Close Price", color="blue")
    plt.plot(df.index, df["moving_avg_3"], label="3-Month Moving Average", linestyle="--", color="red")
    plt.plot(df.index, df["moving_avg_6"], label="6-Month Moving Average", linestyle="--", color="green")
    plt.plot(df.index, df["moving_avg_12"], label="12-Month Moving Average", linestyle="--", color="orange")
    plt.title(f"{symbol} Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    moving_avg_plot_path = os.path.join('stockreport', f"{symbol}_moving_avg_plot.png")
    try:
        plt.savefig(moving_avg_plot_path)
        plot_paths['moving_avg'] = moving_avg_plot_path
        print(f"Moving Average plot saved as {moving_avg_plot_path}")
    except Exception as e:
        print(f"Error saving Moving Average plot: {e}")
    plt.close()

    # Return all plot paths
    return plot_paths
