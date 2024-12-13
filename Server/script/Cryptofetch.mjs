import dotenv from 'dotenv';
import axios from 'axios';
import { CryptoData } from '../src/models/CryptoSchema.mjs';

dotenv.config();

const APIKEY = process.env.API_KEY2;

// Function to delay execution
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const fetchCrypto = async (symbol) => {
    if (!APIKEY) {
    throw new Error('API_KEY is missing. Please set it in your .env file.');
}
    const url = `https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=${symbol}&market=USD&apikey=${APIKEY}`;

    try {
        const response = await axios.get(url);
        const cryptoData = response.data;
        // console.log(cryptoData)

        if (!cryptoData['Meta Data']) {
            console.error('Meta Data is missing or invalid for symbol:', symbol);
            console.log('API Response:', cryptoData);
            return;
        }

        const metadata = cryptoData['Meta Data'];
        const lastRefreshed = metadata['3. Last Refreshed'];
        const timezone = metadata['4. Time Zone'];

        const monthlyData = [];
        const monthlyTimeSeries = cryptoData['Time Series (Digital Currency Monthly)'];
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
        await CryptoData.updateOne(
            { symbol },
            {
                $set: { lastRefreshed, timezone },
                $addToSet: { monthlyData: { $each: monthlyData } }, // Only add if not already present
            },
            { upsert: true } // Create the document if it doesn't exist
        );

        console.log('crypto data updated/saved successfully for:', symbol);
    } catch (error) {
        console.error('Error fetching crypto data:', error.message);
    }
};

const  fetchCryptoDataWithRateLimiting = async (symbols) => {
  for (const symbol of  symbols) {
    await fetchCrypto(symbol);
    // delay for 15 seconds to comply with 5 requests per minute
    await delay(15000);
  }
};

const cryptoSymbols =  ['BTC', 'DOGE', 'ETH', 'SOL', 'USDT', 'SHIB','XRP'];


// fetchCryptoDataWithRateLimiting(cryptoSymbols)

// fetchCrypto('SHIB')
