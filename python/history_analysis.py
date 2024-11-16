import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
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
    # Add gridlines
    plt.grid(True, color = 'maroon', linestyle = '--', alpha=0.5, linewidth = 0.7)
    # Adjust x-axis date format for better visibility (if necessary)
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', fontsize=12)
    # Show the plot
    plt.tight_layout()  # Adjust layout for better fit
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

    return df


        # Function to generate and save plots as images
def generate_plots(symbol, df):
    print(f"Generating plots for {symbol}")
    # Plot Close Price with Bollinger Bands
    plt.figure(figsize=(14, 7))
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

    # Save the plot as an image
    plot_filename = f"{symbol}_bollinger_plot.png"
    try:
        plt.savefig(plot_filename)
        print(f"Plot saved as {plot_filename}")
        if os.path.exists(plot_filename):
            print(f"File {plot_filename} successfully saved.")
        else:
            print(f"Failed to save {plot_filename}.")
    except Exception as e:
        print(f"Error saving plot: {e}")

    plt.close()  # Close after saving the plot to prevent display issues

    return plot_filename

    # Function to create a PDF report with plots and statistics
def create_pdf_report(symbol, df):
        # Define the folder where the reports will be saved
        stockReports_folder = 'stockreport'

        # Create the folder if it doesn't exist
        if not os.path.exists(stockReports_folder):
            os.makedirs(stockReports_folder)

        # Generate the plot
        plot_path = generate_plots(symbol, df)
        
        # Define the PDF file path (in the 'reports' folder)
        pdf_filename = os.path.join(stockReports_folder),f"{symbol}_stock_report.pdf"

        # Create the PDF
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, f"{symbol} Stock Analysis Report")
        
        # Add plot image if it exists
        if os.path.exists(plot_path):
            c.drawImage(plot_path, 50, 400, width=500, height=300)
        else:
            print(f"Plot file {plot_path} not found. Skipping image.")
            
        # Add summary statistics
        stats = df.describe().to_string()
        text_object = c.beginText(50, 350)
        text_object.setFont("Helvetica", 10)
        text_object.textLines(stats)
        c.drawText(text_object)
        
        # Finalize the PDF
        c.save()
        print(f"PDF report for {symbol} saved as {pdf_filename}")
        
        # Clean up the image file
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
