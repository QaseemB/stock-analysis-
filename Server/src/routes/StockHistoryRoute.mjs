import express from 'express'
const router = express.Router();
import {historicalStockData} from '../controllers/stockHistoryController.mjs';


router.route("/stock/:symbol")
    .get(historicalStockData)

export {router};