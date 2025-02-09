import { fetchStockHistory } from "./fetchStockHistory.mjs";
import { delay } from "../utilities/delay.mjs";

export const fetchStockDataWithRateLimiting = async (
  symbols, 
  updateDB = true, 
  batchSize = 10, 
  delayMs = 60000) => {
  console.log(`Starting parallel fetching with batch size: ${batchSize}`);
  for (const symbol of symbols) {
    console.log(`Fetching data for: ${symbol}`);
    await fetchStockHistory(symbol, updateDB);
    await delay(delayMs); // 15-second delay to comply with API rate limits
  }
};

