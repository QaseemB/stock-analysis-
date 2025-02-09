import { fetchAndUpdateStock} from './fetchAndUpdateStock.mjs'
import { delay } from '../utilities/delay.mjs'
import cron from 'node-cron';


export const updateStockWithRateLimiting = async (symbols) => {
    for (const symbol of symbols) {
        console.log('fetching data for symbol:', symbol)
        await fetchAndUpdateStock(symbol)
        await delay(15000)  
    }
};