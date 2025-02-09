import { HistoricalStock } from "../models/HistoricalSchema.mjs";



export const updateStockInDb = async (symbol, metadata, newMonthlyData) => {
  const { lastRefreshed} = metadata.lastRefreshed;


  try {
    await HistoricalStock.updateOne(
      { symbol },
      {
        $push: {
          monthlyData: {
            $each: [newMonthlyData], // Adds the newMonthlyData to the monthlyData array
            $position: 0, // Ensures the newest data is added to the beginning of the array
          },
        },
        $set: { lastRefreshed }, // Updates the lastRefreshed field
      },
      { upsert: true } // Create the document if it does not exist
    );

    console.log('Stock data updated/saved successfully for:', symbol);
  } catch (error) {
    console.error(`Error updating MongoDB for symbol ${symbol}:`, error.message, error.stack);
  }
};