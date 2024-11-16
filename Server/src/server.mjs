import express from 'express';
import mongoose from "mongoose";
import dotenv from "dotenv";
dotenv.config();
import connectDB from './utilities/connectDB.mjs';
import { fetchStockData } from '../script/alphaAPI.mjs';
import {fetchAndUpdateStock}  from '../script/updateHistory.mjs';
import { fetchHistoryStock } from '../script/stockHistory.mjs';
import { fetchCrypto } from '../script/Cryptofetch.mjs';
import {exec} from 'child_process';
import { logger } from '../src/utilities/logger.mjs';


const app = express();


// Connect to MongoDB
connectDB();

// fetchHistoryStock('META')

// fetchStockData('META')



const logTime = (req, res, next) => {
  console.log('Middleware reached')
  const time = new Date();
  console.log(`-----${time.toLocaleTimeString()}: Received a ${req.method} request to ${req.url}.`);
  next();  // Call the next middleware in the stack
};

app.use(logTime)


app.get('/', (req, res) => {
  res.send('Hello, world!');
});

app.get('/api/stock-analysis', (req, res) => {
    exec('python3 history_analysis.py',{cwd: '/Users/qaseembarnhardt/Desktop/CODING/StockMarket/python'}, (error, stdout, stderr) => {
      if (error) {
        logger.error(`${error}`)
        logger.error(`atderr: ${stderr}`)
        logger.error(`stdout ${stdout}`)
       return res.status(500).send({ message: 'python script execution failed' });
      }
       // Send the analysis result back to React (e.g., JSON or path to image)
        res.json({ data: stdout });
    })
});

// Start the server on the specified port, defaulting to 3030
const PORT = process.env.PORT ;
app.listen(PORT, () =>{
  console.log(`Server is running on port ${PORT}`);
})