import axios from 'axios';
import { config } from '../utilities/config.mjs';


export const pythonAnalyzeStock = async (req, res) => {
    const { symbol } = req.params;
    const { date, limit } = req.query;
    const flaskUrl = config.FLASK_API_URL

    if (!symbol) {
        return res.status(400).send({ error: 'Stock symbol is required' });
    }
    try {
        // Call the Flask API for analysis
        const response = await axios.get(`${flaskUrl}/${symbol}`, {
            params: { date, limit }
        });
        // console.log('Flask API response:', response.data);
        
        // Send the analysis data and visualization back to React via Node
        res.json(response.data);
    } catch (error) {
        console.error('Error calling Flask API:', error.message);
        res.status(500).send({ error: 'Error retrieving data from Flask', details: error.message });
    }
};