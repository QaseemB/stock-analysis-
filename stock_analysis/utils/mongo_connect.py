from pymongo import MongoClient
from stock_analysis.config.settings import config



client = MongoClient(config["ATLASURI"])
        
        # Access the database
db = client[config["DB_NAME"]]