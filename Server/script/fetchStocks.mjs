import { fetchStocksInBatches } from "../src/services/fetchStocksInBatches.mjs"
import connectDB from "../src/utilities/connectDB.mjs";
import mongoose from "mongoose";

const stockSymbols = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
  'IBM','TSLA','NVDA','AVGO','TSM','JPM','MA',
  'COST','PG','NFLX','JNJ','BAC','CRM','TM','KO','ORCL', 'D', 'HD', 'ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE',
  'AMD', 'T', 'VZ', 'DIS', 'NKE', 'PFE', 'PEP', 'CSCO', 'CMCSA', 'XOM', 
  'WMT', 'BMY', 'INTC', 'UNH', 'CVX', 'LLY', 'MCD', 'HON', 'NEE', 'TXN', 
  'PM', 'LOW', 'UPS', 'SCHW', 'MS', 'AMGN', 'CAT', 'GS', 'RTX', 'SPGI', 
  'BLK', 'BKNG', 'ISRG', 'MDT', 'SYK', 'LMT', 'DE', 'ADP', 'NOW', 'TMO', 
  'UNP', 'AMT', 'CB', 'CCI', 'ZTS', 'GILD', 'FIS', 'EL', 'MO', 'DUK', 
  'SO', 'MMM', 'BDX', 'APD', 'C', 'USB', 'PNC', 'CL', 'DHR', 'ITW', 'WM', 
  'SHW', 'ECL', 'FISV', 'AON', 'HUM', 'PSA', 'NSC', 'ETN', 'ROP', 'MAR', 
  'KMB', 'AEP', 'SBUX', 'LRCX', 'ATVI', 'ORLY', 'MCO', 'KLAC', 'CTAS', 
  'EQIX', 'ILMN', 'REGN', 'IDXX', 'MTD', 'CDNS', 'SNPS', 'FTNT', 'PAYC', 
  'ANSS', 'VRSK', 'MSCI', 'FLT', 'CPRT', 'TDG', 'WST', 'RMD', 'ALGN', 
  'STE', 'TECH', 'BIO', 'TER', 'KEYS', 'HUBS', 'SEDG', 'ENPH', 'TEAM', 
  'OKTA', 'ZS', 'CRWD', 'DDOG', 'DOCU', 'FSLY', 'NET', 'PLUG', 'BLD', 
  'PTON', 'ROKU', 'SQ', 'TWLO', 'U', 'ZM', 'ZSAN'
];

const stockstack1 = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'IBM', 'TSLA', 'NVDA', 'AVGO', 'TSM', 
                     'JPM', 'MA', 'COST', 'PG', 'NFLX', 'JNJ', 'BAC', 'CRM', 'TM', 'KO', 
                     'ORCL', 'D', 'HD', 'ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE'];

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



const runFetchStockss = async (symbols) => {
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

    await fetchStocksInBatches(symbols)
    console.log("Stock updates completed.");
  } catch (error) {
    console.error("Error during stock updates:", error.message);
  } finally {
  }
}
// run the stocks updates
runFetchStockss(stockstack7)