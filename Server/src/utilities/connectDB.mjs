import mongoose from "mongoose";
import dotenv from 'dotenv';
dotenv.config();

const connectDB = async () => {
    try { 
        const conn = await mongoose.connect(process.env.ATLAS_URI) 
            console.log('Connected to Mongo')
    }catch  (err) { 
        console.error('error connecting to mongodb ${conn.connection.host')
        process.exit(1);
    }
}

export  default connectDB;  //export the function to use it in other files