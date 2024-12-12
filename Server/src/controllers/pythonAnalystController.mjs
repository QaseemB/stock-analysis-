import axios from 'axios';


export const pythonAnalyzeStock = async (req, res) => {
    const { symbol } = req.params;
    const { date, limit } = req.query;

    if (!symbol) {
        return res.status(400).send({ error: 'Stock symbol is required' });
    }
    try {
        // Call the Flask API for analysis
        const response = await axios.get(`http://127.0.0.1:5000/api/analyze/${symbol}`,);
        
        // Send the analysis data and visualization back to React via Node
        res.json(response.data);
    } catch (error) {
        console.error('Error calling Flask API:', error);
        res.status(500).send({ error: 'Error retrieving data from Flask' });
    }
};