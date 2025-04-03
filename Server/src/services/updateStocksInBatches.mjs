import { fetchAndUpdateStock} from './fetchAndUpdateStock.mjs'
import { delay } from '../utilities/delay.mjs'


const BATCH_SIZE = 25

const DELAY_MS = 60000

export const updateStocksInBatches = async (symbols) => {
    const  results = []

    // split stocks into batches
    for (let i = 0; i < symbols.length; i += BATCH_SIZE) {
        const batch = symbols.slice(i, i + BATCH_SIZE)
        console.log(`Fetching Batch:${batch.join(',')}`)

        //parallel fetch for each batch
        const batchResults = await Promise.all(batch.map(fetchAndUpdateStock));
        results.push(...batchResults);

        //delay befor enext batch (execpt for last batch)
        if (i + BATCH_SIZE < symbols.length) {
            console.log(`Waiting ${DELAY_MS/10000} seconds before next batch....` )
            await delay(DELAY_MS)
            }
    }


}