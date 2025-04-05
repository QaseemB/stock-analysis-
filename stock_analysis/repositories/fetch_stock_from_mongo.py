from utils.get_mongo_collection import get_mongo_collection
from config.settings import config 

def fetch_stock_from_mongo(symbol):

    collection = get_mongo_collection(config)
    return collection.find_one({"symbol": symbol})