import { HistoricalStock } from "../models/HistoricalSchema.mjs";


export const historicalStockData = async (req,res) => {
    try{
        const stockHistory = await HistoricalStock.findOne({symbol: req.params.symbol});
        // console.log(stockHistory)
        if(!stockHistory){
            return res.status(404).json({message: "No historical stock data found"});
            }
        res.json(stockHistory)
    }catch(error){
        res.status(500).json({message: error.message});
    }
};