from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()



ATLAS_URI = os.getenv('ATLAS_URI')
client = MongoClient(ATLAS_URI)
db = client["StockMarket"] 
collection = db["historicalstocks"] 


# Fetch a sample document
sample_document = collection.find_one()
# print(sample_document)


def infer_schema(document):
    schema = {}
    for key, value in document.items():
        schema[key] = type(value)  # Use type() to determine the type of each value
    return schema

# Get the schema from the sample document
schema = infer_schema(sample_document)
print(schema)