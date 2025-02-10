import { config } from "../src/utilities/config.mjs";
import { getMongoCollection } from "../src/utilities/getRawDataCollection.mjs";

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

const testSymbol = "MSFT"; 

// Clean stock data in MongoDB (remove duplicates)
async function cleanStockData(symbol) {
   if (!symbol) {
    console.error("❌ No symbol provided.");
    return;
  }

  const collection = await getMongoCollection();
  if (!collection) {
    console.error("❌ Failed to retrieve MongoDB collection.");
    return;
  }

//   console.log(`🔍 Checking for duplicate dates inside 'monthlyData' for ${symbol}`);
console.log(`🔍 Querying collection: ${collection.collectionName}`);

const documents = await collection.find({ symbol: "MSFT" }).toArray();

console.log("Test Query Result:", documents);

  console.log(documents)
  for (let doc of documents) {
    let seenDates = new Set();
    let cleanedMonthlyData = [];

    for (let entry of doc.monthlyData) {
      if (!seenDates.has(entry.date)) {
        seenDates.add(entry.date);
        cleanedMonthlyData.push(entry);
      }
    }

    // Only update if duplicates were found
    if (cleanedMonthlyData.length !== doc.monthlyData.length) {
      await collection.updateOne(
        { _id: doc._id },
        { $set: { monthlyData: cleanedMonthlyData } }
      );
      console.log(`✅ Removed duplicates in 'monthlyData' for ${symbol}.`);
    }
  }
}

cleanStockData(testSymbol)

// npm run cleanRawData