from stock_analysis.repositories.fetch_stock_from_mongo import fetch_stock_from_mongo
from stock_analysis.transfomer.transform_monthly_data import transform_monthly_data
import pandas as pd

def get_stock_data(symbol):
    try:
        # Connect to MongoDB
        stock_data = fetch_stock_from_mongo(symbol)
        if not stock_data:
            print(f"No data found for {symbol}")
            return None
        # Retrieve the monthlyData field
        monthly_data = stock_data.get("monthlyData", [])
        cleaned_data = transform_monthly_data(monthly_data)

        # Inject the symbol into every entry
        for entry in cleaned_data:
            entry["symbol"] = symbol

        # Convert the data into a DataFrame
        df = pd.DataFrame(cleaned_data)
        # print("Columns:", df.columns)
        # print("Unique symbols:", df["symbol"].unique())     


        return df

    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None

# AAPL_data = get_stock_data('AAPL')
# print(AAPL_data)