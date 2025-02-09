from utils.config import config
from utils.get_mongo_collection import get_mongo_collection

collection = get_mongo_collection(config)

# Fetch all stock documents
stocks = collection.find({}, {"symbol": 1, "monthlyData": 1})

total_removed = 0

for stock in stocks:
    symbol = stock["symbol"]
    monthly_data = stock["monthlyData"]

    # Dictionary to track unique dates
    seen_dates = {}
    cleaned_data = []

    for entry in monthly_data:
        date = entry["date"]
        if date not in seen_dates:
            seen_dates[date] = True
            cleaned_data.append(entry)  # Keep the first occurrence

    # Update the document with deduplicated monthlyData
    result = collection.update_one({"_id": stock["_id"]}, {"$set": {"monthlyData": cleaned_data}})
    removed_count = len(monthly_data) - len(cleaned_data)
    total_removed += removed_count

    if removed_count > 0:
        print(f"🧹 Removed {removed_count} duplicates from {symbol}")

print(f"✅ Finished! Total duplicates removed: {total_removed}")
