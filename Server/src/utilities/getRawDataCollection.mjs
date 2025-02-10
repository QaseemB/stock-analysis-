import mongoose from "mongoose";
import { config as mongo } from "../utilities/config.mjs"; // Renamed import to avoid confusion

export async function getMongoCollection() {
  try {
    console.log("MongoDB Database:", mongo.DB_NAME);

    // Ensure required config values exist
    if (!mongo.DB_Collection) {
      throw new Error("DB_COLLECTION is missing in the configuration.");
    }

    // MongoDB connection URI
    const url = mongo.MONGODB_URI || "mongodb://localhost:27017"; // Use your MongoDB URI

    // Connect to MongoDB using Mongoose
    await mongoose.connect(url, {
      dbName: mongo.DB_NAME,
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log("✅ Connected to MongoDB successfully");

    // Access collection
    const collection = mongoose.connection.collection(mongo.DB_Collection);
    return collection;
  } catch (error) {
    console.error("❌ Error connecting to MongoDB:", error);
    throw error;
  }
}


    
//npm run cleanRawData