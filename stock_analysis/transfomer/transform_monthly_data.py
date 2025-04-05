import pandas as pd 

def transform_monthly_data(monthly_data):
    
    for entry in monthly_data:
        if isinstance(entry.get("date"), str):  # Check if the date is stored as a string
            # Convert date string to datetime object
            entry["date"] = pd.to_datetime(entry["date"], errors='coerce')
    
        # Convert '_id' to string for JSON serialization
        entry["_id"] = str(entry.get("_id"))
