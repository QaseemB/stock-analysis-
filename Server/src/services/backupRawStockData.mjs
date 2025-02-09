import {S3Module} from '../utilities/connectS3.mjs'
import {fetchStockApi} from '../utilities/fetchStockApi.mjs'
import {delay} from '../utilities/delay.mjs'

export const backupRawStockData = async (symbols) => {
  const {createStockS3Client,uploadFile,ensureBucketExists} = S3Module;

  const bucketName = "stock-market-analysis-qb";


  try{
    const s3client = await createStockS3Client();
    await ensureBucketExists(s3client, bucketName);

     for (const symbol of symbols){
    try{
       // Fetch data for stock symbols
    const rawData = await fetchStockApi(symbol);
    if (!rawData || rawData["Error Message"]) {
      console.error("API Response Error:", rawData);
      continue;
    }
    console.log(`Retrying after 15 seconds...`);
    await delay(15000);
    // prepare file details
    const fileKey = `raw-data/${symbol}.json`;
    const fileContent = JSON.stringify(rawData);

    //upload file to s3
    await uploadFile(s3client, bucketName, fileKey, fileContent);
    console.log(`Uploaded ${symbol} data to S3`);
    }catch(error) {
        console.error(`Error uploading ${symbol} data to S3:`, error.message);
      }
   };
  } catch(error){
    console.error(`Error creating S3 client or ensuring bucket exists:`, error.message);
    }

 
};
