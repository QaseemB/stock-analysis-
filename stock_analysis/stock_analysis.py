import pandas as pd 
from pymongo import MongoClient 
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


# Connect to MongoDB
ATLAS_URI =  os.getenv('ATLAS_URI')
client = MongoClient(ATLAS_URI)
db = client['StockMarket']
collection = db['stocks']

# Fetch stock data from MongoDB
data = list(collection.find({}))
print("Raw Data Retrieved from MongoDB:", data)  # Check what the raw data looks like

# Convert data to DataFrame
df = pd.DataFrame(data)


# Check the DataFrame structure again
print("DataFrame Structure:\n", df.info())
print("Columns in DataFrame:", df.columns.tolist())

# Print DataFrame columns for verification
print(df.columns)

# Check if 'price' column exists and calculate the average closing price if it does
if 'price' in df.columns:
     # Ensure 'price' column has valid numeric values
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert non-numeric to NaN
    df.dropna(subset=['price'], inplace=True)  # Remove NaN values

     # Calculate the average price
    average_price = df['price'].mean()
    print(f'Average Closing Price: {average_price}')

    # Example: Save results back to MongoDB
    results_collection = db['analysis_results']
    results_collection.insert_one({'average_price': average_price})
else:
    print("Price column not found in DataFrame.")





# print("Connected to database:", db.name)
# print("Using collection:", collection.name)


# data = list(collection.find({}, {'price': 1})) 
# print("Raw Data Retrieved from MongoDB:", data)

