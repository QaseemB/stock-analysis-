import { updateStocksInBatches } from "../src/services/updateStocksInBatches.mjs"
import connectDB from '../src/utilities/connectDB.mjs';
import mongoose from "mongoose";

import cron from 'node-cron';

const stockSymbols = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
  'IBM','TSLA','NVDA','AVGO','TSM',
  'JPM','MA','COST','PG','NFLX','JNJ',
  'BAC','CRM','TM','KO'
];

const stockstack1 = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'IBM', 'TSLA', 'NVDA', 'AVGO', 'TSM', 
                     'JPM', 'MA', 'COST', 'PG', 'NFLX', 'JNJ', 'BAC', 'CRM', 'TM', 'KO', 
                     'ORCL', 'D', 'HD', 'ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE']
const stockstack2 = ['AMD', 'T', 'VZ', 'DIS', 'NKE', 'PFE', 'PEP', 'CSCO', 'CMCSA', 'XOM', 
                     'WMT', 'BMY', 'INTC', 'UNH', 'CVX', 'LLY', 'MCD', 'HON', 'NEE', 'TXN', 
                     'PM', 'LOW', 'UPS', 'SCHW', 'MS', 'AMGN', 'CAT', 'GS', 'RTX', 'SPGI'];
const stockstack3 = ['BLK', 'BKNG', 'ISRG', 'MDT', 'SYK', 'LMT', 'DE', 'ADP', 'NOW', 'TMO', 
                     'UNP', 'AMT', 'CB', 'CCI', 'ZTS', 'GILD', 'FIS', 'EL', 'MO', 'DUK', 
                     'SO', 'MMM', 'BDX', 'APD', 'C', 'USB', 'PNC', 'CL', 'DHR', 'ITW'];
const stockstack4 = ['WM', 'SHW', 'ECL', 'FISV', 'AON', 'HUM', 'PSA', 'NSC', 'ETN', 'ROP', 
                     'MAR', 'KMB', 'AEP', 'SBUX', 'LRCX', 'ATVI', 'ORLY', 'MCO', 'KLAC', 'CTAS', 
                     'EQIX', 'ILMN', 'REGN', 'IDXX', 'MTD', 'CDNS', 'SNPS', 'FTNT', 'PAYC', 'ANSS'];
const stockstack5 = ['VRSK', 'MSCI', 'FLT', 'CPRT', 'TDG', 'WST', 'RMD', 'ALGN', 'STE', 'TECH', 
                     'BIO', 'TER', 'KEYS', 'HUBS', 'SEDG', 'ENPH', 'TEAM', 'OKTA', 'ZS', 'CRWD', 
                     'DDOG', 'DOCU', 'FSLY', 'NET', 'PLUG', 'BLD', 'PTON', 'ROKU', 'SQ', 'TWLO'];
const stockstack6 = ['U', 'ZM', 'ZSAN','VOO','QQQ','DIA', 'VTI'];


const stockStacks = [
  stockstack1,
  stockstack2,
  stockstack3,
  stockstack4,
  stockstack5,
  stockstack6,
];
cron.schedule('0 16 * * *', async () => {
    logger.info('Running scheduled stock data update...');
    try{
      await connectDB()

      if (mongoose.connection.readyState !== 1){
      console.log("MongoDB connection is not established. Aborting operation.");
      return;
    }
    const today = new Date();
    const dayOfMonth = today.getDate(); // e.g., 1, 2, 3, ...

    if (dayOfMonth >= 1 && dayOfMonth <= stockStacks.length) {
      const symbolsToday = stockStacks[dayOfMonth - 1]; // index 0 = 1st day
      logger.info(`📈 Running stockstack for Day ${dayOfMonth}: ${symbolsToday.length} symbols`);
      await updateStocksInBatches(symbolsToday);
    } else {
      logger.info(`📅 No stockstack scheduled for Day ${dayOfMonth}.`);
    }

  } catch (error) {
    console.error("Error during scheduled stock updates:", error.message);
  } finally {
    mongoose.connection.close();
  }
});

const runStockUpdates = async (symbols) => {
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

    await updateStocksInBatches(symbols)
    console.log("Stock updates completed.");
  } catch (error) {
    console.error("Error during stock updates:", error.message);
  } finally {
  }
}
// run the stocks updates
runStockUpdates(stockstack6)

