from pymongo import MongoClient
from stock_analysis.config.settings import config
from stock_analysis.utils.mongo_connect import client, db


def get_mongo_collection(config):

    try:
        # Ensure the configuration key exists
        if "DB_RAW_COLLECTION" not in config:
            raise KeyError("DB_RAW_COLLECTION is missing in the configuration.")
        
        # Access the collection
        collection_name = config["DB_RAW_COLLECTION"]
        collection = db[collection_name]

        return collection
    except KeyError as ke:
        print(f"configuration error: {ke}")
        raise 
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise 