import { HistoricalStock } from "../models/HistoricalSchema.mjs";
import moment from "moment";



export const updateStockInDb = async (symbol, metadata, newMonthlyData) => {
  const lastRefreshed = metadata.lastRefreshed;
  newMonthlyData.date = String(newMonthlyData.date);
  const currentDate = moment(newMonthlyData.date, "YYYY-MM-DD")

  const docExists = await HistoricalStock.findOne({ symbol });
if (!docExists) {
    await HistoricalStock.create({
        symbol: symbol,
        monthlyData: [], // Initializing the array during creation
        lastRefreshed: lastRefreshed
    });
}

console.log("Checking if document exists for symbol:", symbol);
console.log("Document exists:", !!docExists);
console.log("Pushing new data to monthlyData and updating lastRefreshed for symbol:", symbol);


  try {

      // Check if an entry for this month and year already exists
        const existingData = await HistoricalStock.findOne({
            symbol,
            "monthlyData.date": {
                $regex: `${currentDate.format('YYYY-MM')}`, // Regex to match the year and month
            }
        });
if (existingData) {
    console.log(`Data for ${symbol} up to ${currentDate.format('YYYY-MM')} already exists. Skipping update.`);
            return; // Skip updating since the data for this month already exists
        }
  
  
//   // First, remove any existing entries with the same date
// await HistoricalStock.updateOne(
//   { symbol },
//   {
//     $pull: { monthlyData: { date: newMonthlyData.date } }
//   }
// );

// Then, if the document still exists, push the new data and update lastRefreshed
await HistoricalStock.updateOne(
  { symbol },
  {
    // $setOnInsert: { monthlyData: [] }, // Ensures monthlyData exists when inserting new symbols
    $push: {
      monthlyData: {
        $each: [newMonthlyData],
        $position: 0  // Ensures the newest data is added to the beginning of the array
      }
    },
    $set: { lastRefreshed } // Updates the lastRefreshed field
  },
  { upsert: true }
);

    console.log('Stock data updated/saved successfully for:', symbol);
  } catch (error) {
    console.error(`Error updating MongoDB for symbol ${symbol}:`, error.message, error.stack);
  }
};