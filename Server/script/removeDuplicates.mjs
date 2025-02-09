import { config } from "../src/utilities/config.mjs";
import connectDB from "../src/utilities/db.mjs";

//  const removeDuplicates = async () => {
//     try {
//         await connectDB();
//         const db = connectDB.db('StockMarket');
//         const collection = db.collection('historicalStocks');

//         const duplicates = await collection.aggrefate([
//             {
//                 $group: {
//                     _id: {symbol: "$symbol", 
//                     lastRefreshed: "$date",},
//                     documents: { $push: "$_id" }
                    
//                 }
//             }
//         ])
//     }
//  }