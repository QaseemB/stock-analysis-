
import { mongoose } from 'mongoose';
import { parseStockData } from "../utilities/parseStockData.mjs";
import { checkIfDataExists } from "../utilities/checkIfDataExists.mjs";
import { checkIfDataExistsForHistory } from "../utilities/checkIfDataExistforHistory.mjs";
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

    if (!data || !data["Meta Data"]) {
      console.error("Invalid Meta Data for symbol:", symbol);
      console.log("API Response:", data);
      return;
    }

     const {metadata} = parseStockData(data)
    const { monthlyTimeSeries,monthlyData } = metadata;

    
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
    
   
    const newMonthlyData = monthlyData[0]

    console.log(`DEBUG - New Monthly Data:${symbol}`, newMonthlyData);

    const latestDate = monthlyData[0].date;

    
    //check if data exists
    const dataExists = await checkIfDataExistsForHistory (symbol, newMonthlyData,)
    
    console.log(`DEBUG - Data Exists for ${symbol}:`, dataExists);

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