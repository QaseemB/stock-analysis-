import dotenv from 'dotenv';
import axios from 'axios';
import { HistoricalStock } from '../src/models/HistoricalSchema.mjs';

dotenv.config();

const APIKEY = process.env.API_KEY;

// Function to delay execution
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const fetchHistoryStock = async (symbol) => {
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=${symbol}&interval=5min&apikey=${APIKEY}`;

    try {
        const response = await axios.get(url);
        const historyData = response.data;

        if (!historyData['Meta Data']) {
            console.error('Meta Data is missing or invalid for symbol:', symbol);
            console.log('API Response:', historyData);
            return;
        }

        const metadata = historyData['Meta Data'];
        const lastRefreshed = metadata['3. Last Refreshed'];
        const timezone = metadata['4. Time Zone'];

        const monthlyData = [];
        const monthlyTimeSeries = historyData['Monthly Time Series'];
        if (!monthlyTimeSeries) {
            console.error('Monthly Time Series is missing or invalid for symbol:', symbol);
            return;
        }

        for (const [date, stats] of Object.entries(monthlyTimeSeries)) {
            monthlyData.push({
                date,
                open: parseFloat(stats['1. open']),
                high: parseFloat(stats['2. high']),
                low: parseFloat(stats['3. low']),
                close: parseFloat(stats['4. close']),
                volume: parseFloat(stats['5. volume']),
            });
        }

        // Update the document in MongoDB
        await HistoricalStock.updateOne(
            { symbol },
            {
                $set: { lastRefreshed, timezone },
                $addToSet: { monthlyData: { $each: monthlyData } }, // Only add if not already present
            },
            { upsert: true } // Create the document if it doesn't exist
        );

        console.log('Stock data updated/saved successfully for:', symbol);
    } catch (error) {
        console.error('Error fetching stock data:', error.message);
    }
};

const  fetchStockDataWithRateLimiting = async (symbols) => {
  for (const symbol of  symbols) {
    await fetchHistoryStock(symbol);
    // delay for 15 seconds to comply with 5 requests per minute
    await delay(15000);
  }
};

const stockSymbols =  ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'IBM','TSLA'];

const stockSymbols2 = ['NVDA','AVGO','TSM','JPM','MA','COST','PG','NFLX','JNJ','BAC','CRM','TM','KO']


// fetchStockDataWithRateLimiting(stockSymbols2)

// fetchHistoryStock('TSLA')