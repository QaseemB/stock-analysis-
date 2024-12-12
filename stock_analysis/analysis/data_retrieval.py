import pandas as pd
from pymongo import MongoClient
from utils.config import ATLAS_URI

def get_stock_data(symbol):
    try:
        # Connect to MongoDB
        client = MongoClient(ATLAS_URI)
        db = client["StockMarket"]
        collection = db["historicalstocks"]
        
        # Fetch the stock data for the given symbol
        stock_data = collection.find_one({"symbol": symbol})
        if not stock_data:
            print(f"No data found for {symbol}")
            return None
        
        # Print the full stock data to debug the structure
        # print("Stock Data:", stock_data)
        
        # Retrieve the monthlyData field
        monthly_data = stock_data.get("monthlyData", [])
        # print ("Monthly Data:", monthly_data)
        # Convert 'date' column in each entry to datetime (if it's a string)
        for entry in monthly_data:
            if isinstance(entry.get("date"), str):  # Check if the date is stored as a string
                # Convert date string to datetime object
                entry["date"] = pd.to_datetime(entry["date"], errors='coerce')
                # print(f"Converted date: {entry['date']} for entry: {entry}")

            # Convert '_id' to string for JSON serialization
            entry["_id"] = str(entry.get("_id"))

        # Optional: Convert the data into a DataFrame
        df = pd.DataFrame(monthly_data)

        # Optional: Print the first few entries to check date conversion
        # print(df.head())  # Display the first few rows of the DataFrame
        # print("Data types:", df.dtypes)

        return df

    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None
