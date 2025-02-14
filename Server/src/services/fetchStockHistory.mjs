import { mongoose } from "mongoose";
import { fetchStockApi } from "../utilities/fetchStockApi.mjs";
import { updateStockInDb } from "../utilities/updateDb.mjs";
import { parseStockData } from "../utilities/parseStockData.mjs";
import { checkIfDataExistsForHistory } from "../utilities/checkIfDataExistforHistory.mjs";
import { HistoricalStock } from "../models/HistoricalSchema.mjs";
import { logger } from "../utilities/logger.mjs";

export const fetchStockHistory = async (symbol, updateDB = true) => {
    if (mongoose.connection.readyState !== 1) {
      1 = connected
      console.error("MongoDB connection is not established. Aborting operation.");
      return;
    }
  try {
    const data = await fetchStockApi(symbol);

    if (!data || !data["Meta Data"]) {
      console.error("Invalid Meta Data for symbol:", symbol);
      console.log("API Response:", data);
      return;
    }
    const { metadata } = parseStockData(data);
    const { monthlyTimeSeries, lastRefreshed, 
      timezone, monthlyData } =
 metadata;

    // Ensure monthlyData is always an array (if null or undefined, make it an empty array)
    if (!Array.isArray(monthlyData)) {
      monthlyData = [];
      console.warn(
        `Warning: monthlyData is not an array for symbol: ${symbol}. It has been initialized as an empty array`
      );
    }

    if (!monthlyTimeSeries) {
      console.error(
        "Monthly Time Series is missing or invalid for symbol:",
        symbol
      );
      return;
    }

    // Update the document in MongoDB
    if (updateDB) {
      const result = await HistoricalStock.updateOne(
        { symbol },
        {
          $set: { lastRefreshed, timezone },
          $addToSet: { monthlyData: { $each: monthlyData } }, // Only add if not already present
        },
        { upsert: true } // Create the document if it doesn't exist
      );
      logger.info(
        `Stock ${symbol} - Matched: ${result.matchedCount}, Modified: ${
          result.modifiedCount
        }, Upserted: ${result.upsertedCount || 0}`
      );

      if (result.upsertedCount > 0) {
        console.log(`✅ Stock ${symbol} was inserted as a new record.`);
      } else if (result.modifiedCount > 0) {
        console.log(`🔄 Stock ${symbol} was updated with new data.`);
      } else {
        console.log(`⚠️ Stock ${symbol} was found but no new data was added.`);
      }
    } // End of updateDB if statement
    console.log("Stock data updated/saved successfully for:", symbol);
  } catch (error) {
    console.error(
      "Error fetching stock history for symbol:",
      symbol,
      error.message
    );
  }
};
