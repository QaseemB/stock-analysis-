import { HistoricalStock } from '../models/HistoricalSchema.mjs';

/**
 * Processes a single symbol: fetches data from MongoDB and uploads it to S3.
 * @param {Object} s3client - The S3 client.
 * @param {string} bucketName - The S3 bucket name.
 * @param {string} symbol - The stock symbol.
 * @param {Function} uploadFile - The S3 upload function.
 */

export const processSymbol = async (s3client, bucketName, symbol, uploadFile) => {
  try {
    // Fetch stock data from MongoDB
    const stockHistory = await HistoricalStock.findOne({ symbol }).lean();
    if (!stockHistory) {
      console.warn(`No historical data found for ${symbol}, skipping...`);
      return;
    }

    // Prepare file details
    const fileKey = `raw-data/${symbol}.json`;
    const fileContent = JSON.stringify(stockHistory);

    // Upload file to S3
    await uploadFile(s3client, bucketName, fileKey, fileContent);
    console.log(`Uploaded ${symbol} data to S3`);
  } catch (error) {
    console.error(`Error uploading ${symbol} data to S3:`, error.message);
  }
};