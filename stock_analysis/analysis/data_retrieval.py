from pymongo import MongoClient
from utils.config import ATLAS_URI

def get_stock_data(symbol):
    try:
        client = MongoClient(ATLAS_URI)
        db = client["StockMarket"]
        collection = db["historicalstocks"]
        stock_data = collection.find_one({"symbol": symbol})
        if not stock_data:
            print(f"No data found for {symbol}")
            return None
        return stock_data.get("monthlyData", [])
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None