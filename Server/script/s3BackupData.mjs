import {backupRawStockData} from '../src/services/backupRawStockData.mjs'

const stockSymbols = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
  'IBM','TSLA','NVDA','AVGO','TSM','JPM','MA',
  'COST','PG','NFLX','JNJ','BAC','CRM','TM','KO','ORCL', 'D', 'HD', 'ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE',
  'AMD', 'T', 'VZ', 'DIS', 'NKE', 'PFE', 'PEP', 'CSCO', 'CMCSA', 'XOM', 
  'WMT', 'BMY', 'INTC', 'UNH', 'CVX', 'LLY', 'MCD', 'HON', 'NEE', 'TXN', 
  'PM', 'LOW', 'UPS', 'SCHW', 'MS', 'AMGN', 'CAT', 'GS', 'RTX', 'SPGI', 
  'BLK', 'BKNG', 'ISRG', 'MDT', 'SYK', 'LMT', 'DE', 'ADP', 'NOW', 'TMO', 
  'UNP', 'AMT', 'CB', 'CCI', 'ZTS', 'GILD', 'FIS', 'EL', 'MO', 'DUK', 
  'SO', 'MMM', 'BDX', 'APD', 'C', 'USB', 'PNC', 'CL', 'DHR', 'ITW', 'WM', 
  'SHW', 'ECL', 'FISV', 'AON', 'HUM', 'PSA', 'NSC', 'ETN', 'ROP', 'MAR', 
  'KMB', 'AEP', 'SBUX', 'LRCX', 'ATVI', 'ORLY', 'MCO', 'KLAC', 'CTAS', 
  'EQIX', 'ILMN', 'REGN', 'IDXX', 'MTD', 'CDNS', 'SNPS', 'FTNT', 'PAYC', 
  'ANSS', 'VRSK', 'MSCI', 'FLT', 'CPRT', 'TDG', 'WST', 'RMD', 'ALGN', 
  'STE', 'TECH', 'BIO', 'TER', 'KEYS', 'HUBS', 'SEDG', 'ENPH', 'TEAM', 
  'OKTA', 'ZS', 'CRWD', 'DDOG', 'DOCU', 'FSLY', 'NET', 'PLUG', 'BLD', 
  'PTON', 'ROKU', 'SQ', 'TWLO', 'U', 'ZM', 'ZSAN'
];
const symbol2 = ['VOO','QQQ','DIA', 'VTI']
backupRawStockData(symbol2)