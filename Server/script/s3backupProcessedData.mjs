import { backupProcessedData } from "../src/services/backupProcessedData.mjs";
import { config } from "../src/utilities/config.mjs";


const dbUri = config.ATLASURI;
const dbName = config.DB_NAME
const collectionName = config.DB_Collection
const bucketName = "stock-market-analysis-qb";
const fileKey = "processed-data/backup.json";

backupProcessedData(dbUri,dbName,collectionName,bucketName,fileKey)