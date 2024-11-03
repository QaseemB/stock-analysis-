import dotenv from  'dotenv';
import axios from 'axios';
import request from 'request-promise-native'; 
import { Stock } from '../src/models/StockSchema.mjs';

dotenv.config();

// const APIKEY = process.env.API_KEY

// Function to delay execution
const delay = (ms) => new  Promise(resolve => setTimeout(resolve, ms));

// Function to fetch stock data with rate limiting
export const fetchStockData = async (symbol) => {
 const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&interval=5min&apikey=${APIKEY}`;

  try  {  
    //fetch stock data
 const response = await axios.get(url);
 if (response.status !== 200) throw new  Error('API Error: ${response.status');


 const stockData = response.data['Global Quote'];
// console.log(stockData)

 const processedData = {
    symbol: stockData['01. symbol'],  // Using '01. symbol' to access the symbol
    open: parseFloat(stockData['02. open']),
    high: parseFloat(stockData['03. high']),
    low: parseFloat(stockData['04. low']),
    price: parseFloat(stockData['05. price']),
    volume: parseInt(stockData['06. volume']),
    tradingDay: stockData['07. latest trading day'], // Access latest trading day
    change: parseFloat(stockData['09. change']),
    changePercent: stockData['10. change percent']
};
console.log('processed Data:', processedData);

 // Check if stock with the same symbol and trading day already exists

const existingStock = await Stock.findOne({
  symbol: processedData.symbol,
  tradingDay: processedData.tradingDay
});

if(existingStock){
        console.log('Stock Already exist with the same tradign day:', existingStock)
        await Stock.updateOne({ _id: existingStock._id }, processedData);
            console.log('Stock data updated in MongoDB');
    } else {
    // If the stock does not exist, create a new stock instance
   const  stock = new Stock(processedData);
   // save to MongoDB
  await stock.save()
  console.log('stock saved to MongoDB');
}
  return processedData;

  }catch(error){
    console.error('error fetching stock data', error)
  }
   return processedData;
};

const  fetchStockDataWithRateLimiting = async (symbols) => {
  for (const symbol of  symbols) {
    await fetchStockData(symbol);
    // delay for 15 seconds to comply with 5 requests per minute
    await delay(15000);
  }
};

const stockSymbols =  ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'IBM'];
// fetchStockDataWithRateLimiting(stockSymbols);

