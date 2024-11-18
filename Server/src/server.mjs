import express from 'express';
import dotenv from "dotenv";
dotenv.config();
import connectDB from './utilities/connectDB.mjs';
import { logger } from '../src/utilities/logger.mjs';
import cors from 'cors';
import {router as analyzeRoute} from './routes/pythonAnalystRoute.mjs';
import {router as stockRoute} from './routes/StockHistoryRoute.mjs'


const app = express();


// Middleware 
app.use(express.json());
app.use(cors({
  origin: '*',
}))


// Connect to MongoDB
connectDB();




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

app.use('api',analyzeRoute)

app.use('/api', stockRoute);


// Start the server on the specified port, defaulting to 3030
const PORT = process.env.PORT ;
app.listen(PORT, () =>{
  console.log(`Server is running on port ${PORT}`);
})