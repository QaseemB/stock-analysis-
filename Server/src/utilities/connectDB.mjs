import mongoose from "mongoose";
import { config } from "./config.mjs";

const connectDB = async () => {
  mongoose.connection.on("connected", () => {
    console.log("Mongoose connected to the database.");
  });

  mongoose.connection.on("error", (err) => {
    console.error("Mongoose connection error:", err);
  });

  mongoose.connection.on("disconnected", () => {
    console.log("Mongoose disconnected.");
  });

  try {
    const conn = await mongoose.connect(config.ATLASURI, {
      serverSelectionTimeoutMS: 30000, // 30 seconds
      socketTImeoutMS: 45000, //45 seconds
    });
    console.log("Database connection established. Starting the server...");
  } catch (err) {
    console.error(`error connecting to mongodb: ${conn.connection.host}`);
    process.exit(1);
  }
};

export default connectDB; //export the function to use it in other files
