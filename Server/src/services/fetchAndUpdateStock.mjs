
import { mongoose } from 'mongoose';
import { parseStockData } from "../utilities/parseStockData.mjs";
import { checkIfDataExists } from "../utilities/checkIfDataExists.mjs";
import { updateStockInDb } from "../utilities/updateDb.mjs";
import { fetchStockApi } from "../utilities/fetchStockApi.mjs";
import { logger } from '../utilities/logger.mjs';


export const fetchAndUpdateStock = async (symbol) =>{
   if (mongoose.connection.readyState !== 1) { // 1 = connected
    console.error("MongoDB connection is not established. Aborting operation.");
    return;
  }
  try{
    const data = await fetchStockApi(symbol)
    //  if (!data || !data.metadata || !data.metadata.monthlyTimeSeries) {
    //   throw new Error(`Invalid or missing data for symbol: ${symbol}`);
    // }
    const {metadata, newMonthlyData} = parseStockData(data)

    const latestDate = Object.keys(metadata.monthlyTimeSeries)[0]
    
    //check if data exists
    const dataExists = await checkIfDataExists(symbol, latestDate)
    if(dataExists){
        logger.info(`Data for ${symbol} up to ${latestDate} already exists. Skipping update.`)
        return;
    }
    //update stock in db
    await updateStockInDb(symbol, metadata, newMonthlyData)
    logger.info(`Data for ${symbol} up to ${latestDate} has been updated.`)
  }catch (error){
    logger.error(`Error fetching and updating stock data for ${symbol}: ${error.message}`)
  }


}