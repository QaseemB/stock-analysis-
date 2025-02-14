
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
    const {metadata} = parseStockData(data)
    const { monthlyTimeSeries, lastRefreshed, 
      timezone, monthlyData } =
    metadata;
    
    const data = await fetchStockApi(symbol)

    if (!data || !data["Meta Data"]) {
      console.error("Invalid Meta Data for symbol:", symbol);
      console.log("API Response:", data);
      return;
    }
    

    const latestDate = Object.keys(monthlyTimeSeries)[0]
    
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