import dotenv from  'dotenv';
import axios from 'axios';
import request from 'request-promise-native'; 

dotenv.config();

const APIKEY = process.env.API_KEY

// Function to fetch stock data
export const fetchStockData = async (symbol) => {
 const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&interval=5min&apikey=${APIKEY}`;
  try  {  
 const response = await axios.get(url);
 console.log(response.status);
 const stockData = response.data['Global Quote'];

 const processedData = {
    symbol: stockData['01. symbol'],  // Using '01. symbol' to access the symbol
    open: parseFloat(stockData['02. open']),
    high: parseFloat(stockData['03. high']),
    low: parseFloat(stockData['04. low']),
    price: parseFloat(stockData['05. price']),
    volume: parseInt(stockData['06. volume']),
    tradingDay: stockData['07. latest trading day'], // Access latest trading day
    change: parseFloat(stockData['09. change']),
    changePercent: stockData['10. change percent']
};
return processedData;
  }catch(error){
    console.error('error fetching stock data', error)
  }
// request.get({
//     url: url,
//     json: true,
//     headers: {'User-Agent': 'request'}
//   }, (err, res, data) => {
//     if (err) {
//       console.log('Error:', err);
//     } else if (res.statusCode !== 200) {
//       console.log('Status:', res.statusCode);
//     } else {
//       // data is successfully parsed as a JSON object:
//       console.log(data);
//     }
// });
};

