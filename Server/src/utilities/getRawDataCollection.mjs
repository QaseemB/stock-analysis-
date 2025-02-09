import mongoose from "mongoose";
import { config } from "./config.mjs";


export async function getMongoCollection(config) {
    try {
    // Ensure the configuration key exists
    if (!config.DB_RAW_COLLECTION) {
      throw new Error("DB_RAW_COLLECTION is missing in the configuration.");
    }

    // MongoDB connection URI and DB details
    const url = config.MONGODB_URI || 'mongodb://localhost:27017'; // Use your MongoDB URI here
    const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

    // Connect to MongoDB
    await client.connect();
    console.log("Connected to MongoDB successfully");

     const db = client.db(config.DB_NAME);  // Replace with your DB name from config
    const collection = db.collection(config.DB_RAW_COLLECTION);  // Collection from config

    return collection;
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
    throw error;
  }
}


    
