import express from 'express';
const router = express.Router();
import { pythonAnalyzeStock } from '../controllers/pythonAnalystController.mjs';


// Define your routes here
router.route('/stock-analysis/:symbol')
    .get(pythonAnalyzeStock);

export {router}; // Export the router to use it in your app.js file