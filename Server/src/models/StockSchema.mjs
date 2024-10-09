const mongoose = require('mongoose');

const stockSchema = new mongoose.Schema({
    symbol: String,
    open: Number,
    high: Number,
    low: Number,
    price: Number,
    volume: Number,
    tradingDay: String,
    change: Number,
    changePercent: String
});

const Stock = mongoose.model('Stock', stockSchema);

async function saveStockData(stock) {
    const newStock = new Stock(stock);
    await newStock.save();
}

module.exports = { saveStockData };