import axios from 'axios';
import { config } from './config.mjs';


const APIKEY = config.APIKEY1
const BASE_URL = config.BASE_URL;

export const fetchStockApi = async (symbol) => {
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=${symbol}&interval=5min&apikey=${APIKEY}`;
  
    try {
        const response = await axios.get(url);
        const data = response.data;
        console.log()

        if (data.Information) { 
      console.error(`API Limit Reached: ${data.Information}`);
      return null;  // Return null so calling functions can handle this case
    }

        return data;

        
    }   catch (error) {
        console.error(`Error fetching api for symbol ${symbol}: ${error.message}`);
        throw error;
    }
};