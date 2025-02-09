from pymongo import MongoClient
from utils.config import config



client = MongoClient(config["ATLASURI"])
        
        # Access the database
db = client[config["DB_NAME"]]