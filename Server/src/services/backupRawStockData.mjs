import { S3Module } from "../utilities/connectS3.mjs";
import connectDB  from "../utilities/connectDB.mjs";
import { processSymbol } from "../utilities/processSymbol.mjs";
import { delay } from "../utilities/delay.mjs";

/**
 * Backs up raw stock data from MongoDB to S3 using batch and parallel processing.
 * @param {Array} symbols - Array of stock symbols.
 * @param {number} batchSize - Number of symbols to process concurrently per batch.
 */

export const backupRawStockData = async (symbols, batchSize = 10) => {
  const { createStockS3Client, uploadFile, ensureBucketExists } = S3Module;

  const bucketName = "stock-market-analysis-qb";

  try {
    // Connect to MongoDB
    await connectDB();

    // Create and prepare S3 client
    const s3client = await createStockS3Client();
    await ensureBucketExists(s3client, bucketName);

    // Process symbols in batches
    for (let i = 0; i < symbols.length; i += batchSize) {
      const batch = symbols.slice(i, i + batchSize);
      console.log(`Processing batch: ${batch.join(", ")}`);

      // Process the batch concurrently using Promise.all
      await Promise.all(
        batch.map((symbol) =>
          processSymbol(s3client, bucketName, symbol, uploadFile)
        )
      );

      // Optionally add a delay between batches to avoid overwhelming resources
      await delay(2000); // delay in milliseconds
    }
    console.log("Backup complete.");
  } catch (error) {
    console.error(`Error during backup process:`, error.message);
  }
};





