import {config} from '../src/utilities/config.mjs'
import express from 'express';
import { validateConfig } from './utilities/configValidation.mjs';
import connectDB from './utilities/connectDB.mjs';
import { logger } from '../src/utilities/logger.mjs';
import cors from 'cors';
import { createStockS3Client as S3Connection } from './utilities/connectS3.mjs';
import { fetchStockDataWithRateLimiting } from '../script/stockHistory.mjs';
import '../script/updateStocks.mjs';
import '../script/s3BackupData.mjs';
import {router as analyzeRoute} from './routes/pythonAnalystRoute.mjs';
import {router as stockRoute} from './routes/StockHistoryRoute.mjs';




const app = express();

// fetchHistoryStock('AAPL')

// Validate configuration
try {
  validateConfig(); 
} catch (error) {
  console.error('Configuration Error:', error.message);
  process.exit(1);
}

// Middleware 
app.use(express.json());
app.use(cors({
  origin: '*',
}));

// Initialize services
try {
  S3Connection();
  // console.log('Connected to S3 successfully.');
} catch (error) {
  console.error('S3 Connection Error:', error.message);
  process.exit(1);
}

const starServer = async () => {
  try {
    await connectDB();
  } catch (error) {
    console.error("Server failed to start due to DB connection issues:", error.message);
    process.exit(1);
  }
};
starServer();

// fetchStockDataWithRateLimiting(['AAPL'])


//Middleware for logging request
const logTime = (req, res, next) => {
  console.log('Middleware reached')
  const time = new Date();
  console.log(`-----${time.toLocaleTimeString()}: Received a ${req.method} request to ${req.url}.`);
  next();  // Call the next middleware in the stack
};

app.use(logTime)

//Routes 
app.use('/api',analyzeRoute)
app.use('/api', stockRoute);

// Centralized error-handling middleware
app.use((err, req, res, next) => {
  logger.error('Unhandled Error:', err.message);
  res.status(500).json({ error: 'Internal Server Error' });
});

// Start the server on the specified port, defaulting to 3030
const PORT = config.PORT || 3030;
app.listen(PORT, () =>{
  console.log(`Server is running on port ${PORT}`);
})

// Graceful shutdown
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error.message);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  process.exit(1);
});