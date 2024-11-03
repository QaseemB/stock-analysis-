import mongoose from "mongoose";

const stockSchema = new mongoose.Schema({
    symbol:{
        type:  String,
        required: true,
    },
    open: Number,
    high: Number,
    low: Number,
    price: Number,
    volume: Number,
    tradingDay: String,
    change: Number,
    changePercent: String,
},{timestamps: true});

stockSchema.index({ symbol: 1, tradingDay: 1 }, { unique: true });

export const Stock = mongoose.model('Stock', stockSchema);

