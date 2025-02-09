import { config } from "../src/utilities/config.mjs";
import { getMongoCollection } from "../src/utilities/getRawDataCollection.mjs";

// Clean stock data in MongoDB (remove duplicates)
async function cleanStockData(symbol) {
  const collection = db.collection(symbol);

  // Example aggregation pipeline to remove duplicates based on symbol and date
  const pipeline = [
    {
      "$group": {
        "_id": { "symbol": "$symbol", "date": "$date" },
        "duplicates": { "$push": "$_id" },
        "count": { "$sum": 1 }
      }
    },
    {
      "$match": { "count": { "$gt": 1 } }
    }
  ];

  const duplicates = await collection.aggregate(pipeline).toArray();

  // Remove duplicates, keeping only the first entry
  for (let entry of duplicates) {
    const duplicateIds = entry.duplicates.slice(1);  // Keep only the first record, delete others
    await collection.deleteMany({ "_id": { "$in": duplicateIds } });
  }
  console.log(`Removed ${duplicates.length} duplicate records for ${symbol}.`);
}