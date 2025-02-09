import {backupRawStockData} from '../src/services/backupRawStockData.mjs'

const stockSymbols = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'IBM',
  'TSLA', 'NVDA', 'AVGO', 'TSM', 'JPM', 'MA',
  'COST', 'PG', 'NFLX', 'JNJ', 'BAC', 'CRM', 'TM', 'KO'
];

backupRawStockData(stockSymbols)