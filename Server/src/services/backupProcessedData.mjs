import { S3Module } from "../utilities/connectS3.mjs";
import { fetchProcessedData } from "../utilities/fetchProcessedData.mjs";

export const backupProcessedData = async (dbUri, dbName, collectionName, bucketName, fileKey) => {
  const { createStockS3Client, uploadFile } = S3Module;

  try {
    const s3client = await createStockS3Client();

    // Fetch processed data
    const processedData = await fetchProcessedData(dbUri, dbName, collectionName);

    if (processedData.length === 0) {
      console.log("No processed data found to back up.");
      return;
    }

    // Prepare data for upload
    const fileContent = JSON.stringify(processedData, null, 2);

    // Upload to S3
    await uploadFile(s3client, bucketName, fileKey, fileContent);
    console.log(`Processed data backed up to S3: ${fileKey}`);
  } catch (error) {
    console.error("Error backing up processed data to S3:", error.message);
  }
};