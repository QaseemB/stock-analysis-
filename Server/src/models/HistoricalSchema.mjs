import mongoose from "mongoose";

const monthlyDataSchema = new mongoose.Schema({
  date: { type: String, required: true,},
  open: { type: Number, required: true },
  high: { type: Number, required: true },
  low: { type: Number, required: true },
  close: { type: Number, required: true },
  volume: { type: Number, required: true }
});

const hisdtoricalStockSchema =  new mongoose.Schema({
        symbol: {type: String,required: true},
        lastRefreshed : {type: Date,required: true},
        timezone: {type: String,required: true},
        monthlyData: [monthlyDataSchema]
    });


export const  HistoricalStock = mongoose.model('HistoricalStock', hisdtoricalStockSchema);
