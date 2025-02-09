import { config } from "./config.mjs";
import { logger } from "./logger.mjs";
import {
  S3Client,
  PutObjectCommand,
  CreateBucketCommand,
  HeadBucketCommand,
  DeleteObjectCommand,
  DeleteBucketCommand,
  paginateListObjectsV2,
  GetObjectCommand,
} from "@aws-sdk/client-s3";


export const createStockS3Client =  async () => {
   const s3Client = new S3Client({
    region: config.S3_REGION, 
    credentials: {
        accessKeyId: config.AWS_ACCESS_KEY_ID,
        secretAccessKey: config.AWS_SECRET_ACCESS_KEY,
  },
});
 try {
    console.log("S3 Client created successfully.");
  } catch (error) {
    console.error("Error initializing S3 client:", error.message);
  }
  return s3Client;
};

export const ensureBucketExists = async (s3client, bucketName) => {
    try {
      const command = new HeadBucketCommand({ Bucket: bucketName });
      await s3client.send(command);
      logger.info(`Bucket ${bucketName} exists.`);
    } catch (error) {
      if (error.name === 'NotFound') {
        logger.warn(`Bucket ${bucketName} not found, creating...`);
        await createBucket(bucketName);
      } else {
        logger.error(`Error ensuring bucket exists: ${error.message}`);
      }
    }
  };

  const createBucket = async (s3client, bucketName) => {
    try {
      const command = new CreateBucketCommand({ Bucket: bucketName });
      await s3client.send(command);
      logger.info(`Bucket ${bucketName} created successfully.`);
    } catch (error) {
      logger.error(`Error creating bucket ${bucketName}: ${error.message}`);
    }
  };

const uploadFile = async (s3client, bucketName, key, fileContent) => {
  await ensureBucketExists(s3client, bucketName);
  try {
    const command = new PutObjectCommand({
      Bucket: bucketName,
      Key: key,
      Body: fileContent,
    });

    const response = await s3client.send(command);
    console.log("File uploaded successfully:", response);
  } catch (error) {
    console.error("Error uploading file:", error);
  }
};


export const S3Module = {
  createStockS3Client,
  ensureBucketExists,
  createBucket,
  uploadFile,
};


