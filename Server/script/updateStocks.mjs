import { updateStockWithRateLimiting } from "../src/services/updateStockWithRateLimiting.mjs";
import connectDB from '../src/utilities/connectDB.mjs';
import mongoose from "mongoose";

import cron from 'node-cron';

const stockSymbols = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
  'IBM','TSLA','NVDA','AVGO','TSM',
  'JPM','MA','COST','PG','NFLX','JNJ',
  'BAC','CRM','TM','KO'
];

cron.schedule('0 16 * * 1-5', async () => {
    logger.info('Running scheduled stock data update...');
    await updateStockWithRateLimiting(stockSymbols);
});

const runStockUpdates = async () => {
  try {
    await connectDB()

    //
    if (mongoose.connection.readyState !== 1) {
      console.log("MongoDB connection is not established. Aborting operation.");
      return;
    }
    console.log("Database connection established. Starting stock updates...");

    // Iterate through stock symbols and fetch/update data
    // for (const symbol of stockSymbols) {
    //   console.log(`Fetching data for symbol: ${symbol}`);
    //   await updateStockWithRateLimiting(symbol); // Your stock update logic
    // }

    await updateStockWithRateLimiting(stockSymbols)
    console.log("Stock updates completed.");
  } catch (error) {
    console.error("Error during stock updates:", error.message);
  } finally {
  }
}
// run the stocks updates
runStockUpdates(stockSymbols)
