from repositories.fetch_stock_from_mongo import fetch_stock_from_moongo
from transfomer.transform_monthly_data import transform_monthly_data
import pandas as pd

def get_stock_data(symbol):
    try:
        # Connect to MongoDB
        stock_data = fetch_stock_from_moongo(symbol)
        if not stock_data:
            print(f"No data found for {symbol}")
            return None
        # Retrieve the monthlyData field
        monthly_data = stock_data.get("monthlyData", [])
        cleaned_data = transform_monthly_data(monthly_data)

        # Convert the data into a DataFrame
        df = pd.DataFrame(cleaned_data)

        return df

    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None
