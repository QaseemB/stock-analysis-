import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import json
from dotenv import load_dotenv
import os
import plotly.express as px
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Load environment variables from .env
load_dotenv()

print("Files in current directory:")
for filename in os.listdir(os.getcwd()):
    print(filename)

# Function to analyze and plot data for a specific stock symbol
def analyze_stock(symbol):
    ATLAS_URI = os.getenv('ATLAS_URI')
    try: 
        client = MongoClient(ATLAS_URI)
        db = client['StockMarket']
        collection = db['historicalstocks']
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None # RETURN if connection fails

    # Retrieve data
    try:       
        stock_data = collection.find_one({"symbol": symbol})
        if not stock_data:
            print(f"No data found for {symbol}")
            return None
    except Exception as e:
         print(f"Error retrieving data: {e}")
         return None

    # Create DataFrame from retrieved data
    df = pd.DataFrame(stock_data.get("monthlyData", []))  # ADDED: Safe access to 'monthlyData'
    if df.empty:
        print(f"No 'monthlyData' found for {symbol}")
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Sort the data by date
    df.sort_index(inplace=True)

     # Ensure necessary columns are present
    if 'close' not in df.columns:
        print("The 'close' column is missing in the data. Cannot proceed with the analysis.")
        return None  # RETURN None IF COLUMN IS MISSING

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

    summary = {
        "symbol": symbol,
        "summary_stats": df.describe().to_dict(),
        "moving_averages": {
            "3_month": df["moving_avg_3"].dropna().to_dict(),
            "6_month": df["moving_avg_6"].dropna().to_dict(),
            "12_month": df["moving_avg_12"].dropna().to_dict()
        },
        "bollinger_bands": {
            "upper_band": df["upper_band"].dropna().to_dict(),
            "lower_band": df["lower_band"].dropna().to_dict()
        },
        "macd": {
            "macd": df['macd'].dropna().to_dict(),
            "signal_line": df['signal_line'].dropna().to_dict()
        }
    }
    return summary

if __name__ == "__main__":
    symbol = "AAPL"
    analysis_result = analyze_stock(symbol)
    print(json.dumps(analysis_result))  # Output the result as JSON



    # Interactive plot using Plotly
    fig = px.line(df, x=df.index, y=["close", "moving_avg_3", "moving_avg_6", "upper_band", "lower_band"],
                  title=f"{symbol} Interactive Stock Analysis")
    fig.update_layout(xaxis_title="Date", yaxis_title="Price")
    fig.show()

    # Print summary statistics
    print(f"Summary for {symbol}:")
    print(df.describe())

    # return df


        # Function to generate and save plots as images
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


def create_pdf_report(symbol, df):
    # Define the folder where the reports will be saved
    stockReports_folder = 'stockreport'

    # Create the folder if it doesn't exist
    if not os.path.exists(stockReports_folder):
        os.makedirs(stockReports_folder)

    # Generate the plots
    plot_paths = generate_plots(symbol, df)

    # Define the PDF file path (in the 'reports' folder)
    pdf_filename = os.path.join(stockReports_folder, f"{symbol}_stock_report.pdf")

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"{symbol} Stock Analysis Report")
    
    y_position = 650  # Starting Y position for content
    margin_left = 50  # Left margin for content
    margin_right = 550  # Right margin for content
    
    # Loop through the plot paths and add them to the PDF
    for plot_type, plot_path in plot_paths.items():
        if os.path.exists(plot_path):
            if y_position < 100:  # Check if there is space for the next image
                c.showPage()  # Start a new page if there isn't enough space
                y_position = 650  # Reset Y position for the new page
            
            # Add the image to the PDF
            c.drawImage(plot_path, margin_left, y_position, width=500, height=300)
            y_position -= 320  # Adjust for next plot

    # Add summary statistics
    stats = df.describe().to_string()
    text_object = c.beginText(50, y_position)
    text_object.setFont("Helvetica", 10)
    text_object.textLines(stats)
    c.drawText(text_object)
    
    # Finalize the PDF
    c.save()
    print(f"PDF report for {symbol} saved as {pdf_filename}")

    # Clean up the image files
    for plot_path in plot_paths.values():
        if os.path.exists(plot_path):
            os.remove(plot_path)



if __name__ == "__main__":
    # List of stock symbols to analyze
    stock_symbols = ['AAPL', 'GOOG', 'AMZN', 'META', 'MSFT', 'TSLA', 'IBM']
    
    # Iterate over each stock symbol and process them
    for symbol in stock_symbols:
        print(f"Processing {symbol}...")
        df = analyze_stock(symbol)

        # Check if df is not None before proceeding
        if df is not None:
            # Generate and save the plot image
            plot_path = generate_plots(symbol, df)
            
            # Create the PDF report with the plot and statistics
            create_pdf_report(symbol, df)
        else:
            print(f"Analysis failed or DataFrame is empty for {symbol}, skipping further steps.")
