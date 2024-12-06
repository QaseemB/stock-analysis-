import matplotlib.pyplot as plt
import os

def save_plot(df, symbol):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["close"], label="Close Price")
    plt.plot(df.index, df["upper_band"], label="Upper Band", linestyle="--")
    plt.plot(df.index, df["lower_band"], label="Lower Band", linestyle="--")
    plt.title(f"{symbol} Analysis")
    plt.legend()
    plot_path = f"stockreport/{symbol}_analysis.png"
    os.makedirs("stockreport", exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    return plot_path
