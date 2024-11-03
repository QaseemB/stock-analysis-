import dotenv from  'dotenv';
import axios from 'axios';
import { HistoricalStock } from '../src/models/HistoricalSchema.mjs';



dotenv.config();

// const APIKEY = process.env.API_KEY

// Function to delay execution
const delay = (ms) => new  Promise(resolve => setTimeout(resolve, ms));


export const fetchAndUpdateStock = async  (symbol) => { 
     const url = `https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=${symbol}&interval=5min&apikey=${APIKEY}`;

     try {
        const response = await axios.get(url);
        const historyData = response.data;
        // console.log(historyData)

        //parse metadata

        const metadata =  historyData['Meta Data'];
        const lastRefreshed = metadata['3. Last Refreshed'];
        const timezone  = metadata['4. Time Zone'];


        // Parse Monthly time series 
        const monthlyData = [];
        const monthlyTimeSeries =  historyData['Monthly Time Series'];
        const latestDate = Object.keys(monthlyTimeSeries)[0];

        // Check if the latest month is already in the database
        const existingEntry = await HistoricalStock.findOne({
            symbol,
            'monthlyData.date': latestDate
        });

           if (existingEntry) {
            console.log(`Data for ${symbol} up to ${latestDate} already exists. Skipping update.`);
            return; // Skip if the latest month is already present
        }

         const newMonthlyData = {
            date: latestDate,
            open: parseFloat(monthlyTimeSeries[latestDate]['1. open']),
            high: parseFloat(monthlyTimeSeries[latestDate]['2. high']),
            low: parseFloat(monthlyTimeSeries[latestDate]['3. low']),
            close: parseFloat(monthlyTimeSeries[latestDate]['4. close']),
            volume: parseFloat(monthlyTimeSeries[latestDate]['5. volume']),
        };

        // Update the database by adding the new month to `monthlyData`
        await HistoricalStock.updateOne(
            { symbol },
            { 
                $push: { monthlyData: {
               $each: [newMonthlyData],
               $position: 0
               }
            }, 
           $set: { lastRefreshed: lastRefreshed } },
            { upsert: true } // Create the document if it does not exist
        );

        console.log('New data for ', symbol, 'up to', latestDate, 'has been added to the database.');

     }catch(error){
    console.error('error fetching stock data', error)
  }
}

const  updateStockDataWithRateLimiting = async (symbols) => {
  for (const symbol of  symbols) {
    await fetchHistoryStock(symbol);
    // delay for 15 seconds to comply with 5 requests per minute
    await delay(15000);
  }
};

const stockSymbols =  ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'IBM',"TSLA"];


// updateStockDataWithRateLimiting(stockSymbols)
// fetchAndUpdateStock('TSLA')
